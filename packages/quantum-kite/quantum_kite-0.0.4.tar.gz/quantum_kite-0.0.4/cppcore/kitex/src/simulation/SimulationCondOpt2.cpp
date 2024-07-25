/***********************************************************/
/*                                                         */
/*   Copyright (C) 2018-2022, M. Andelkovic, L. Covaci,    */
/*  A. Ferreira, S. M. Joao, J. V. Lopes, T. G. Rappoport  */
/*                                                         */
/***********************************************************/




#include "Generic.hpp"
#include "tools/ComplexTraits.hpp"
#include "tools/myHDF5.hpp"
#include "simulation/Global.hpp"
#include "tools/Random.hpp"
#include "lattice/Coordinates.hpp"
#include "lattice/LatticeStructure.hpp"
template <typename T, unsigned D>
class Hamiltonian;
template <typename T, unsigned D>
class KPM_Vector;
#include "tools/queue.hpp"
#include "simulation/Simulation.hpp"
#include "hamiltonian/Hamiltonian.hpp"
#include "vector/KPM_VectorBasis.hpp"
#include "vector/KPM_Vector.hpp"

template <typename T,unsigned D>
void Simulation<T,D>::calc_condopt2(){
    debug_message("Entered Simulation::calc_condopt\n");

    // Make sure that all the threads are ready before opening any files
    // Some threads could still be inside the Simulation constructor
    // This barrier is essential
#pragma omp barrier

  int NMoments, NRandom, NDisorder, direction, special;
  bool local_calculate_condopt2 = false;
#pragma omp master
{
  auto * file = new H5::H5File(name, H5F_ACC_RDONLY);
  Global.calculate_condopt2 = false;
  try{
    int dummy_variable;
    get_hdf5<int>(&dummy_variable,  file, (char *)   "/Calculation/conductivity_optical_nonlinear/NumMoments");
    Global.calculate_condopt2 = true;
  } catch(H5::Exception&) {debug_message("Condopt2: no need to calculate Condopt2.\n");}
  file->close();
  delete file;
}
#pragma omp barrier
#pragma omp critical
  local_calculate_condopt2 = Global.calculate_condopt2;

#pragma omp barrier

if(local_calculate_condopt2){
#pragma omp master
      {
        std::cout << "Calculating the second-order optical conductivity.\n";
      }
#pragma omp barrier
#pragma omp critical
{
    auto * file = new H5::H5File(name, H5F_ACC_RDONLY);

    debug_message("Optical conductivity: checking if we need to calculate Condopt.\n");
    get_hdf5<int>(&direction, file, (char *) "/Calculation/conductivity_optical_nonlinear/Direction");
    get_hdf5<int>(&NMoments, file, (char *)  "/Calculation/conductivity_optical_nonlinear/NumMoments");
    get_hdf5<int>(&NRandom, file, (char *)   "/Calculation/conductivity_optical_nonlinear/NumRandoms");
    get_hdf5<int>(&NDisorder, file, (char *)   "/Calculation/conductivity_optical_nonlinear/NumDisorder");
    get_hdf5<int>(&special, file, (char *)   "/Calculation/conductivity_optical_nonlinear/Special");

    file->close();
    delete file;

}
  CondOpt2(NMoments, NRandom, NDisorder, direction, special);
  }

}
template <typename T,unsigned D>
void Simulation<T,D>::CondOpt2(int NMoments, int NRandom, int NDisorder, int direction, int special){
    std::string dir(num2str3(direction));                                                // xxx Gamma0
    std::string dirc1 = dir.substr(0,1) + "," + dir.substr(1,2);                         // x,xx Gamma1
    std::string dirc2 = dir.substr(0,2) + "," + dir.substr(2,1);                         // xx,x Gamma2
    std::string dirc3 = dir.substr(0,1) + "," + dir.substr(1,1) + "," + dir.substr(2,1); // x,x,x Gamma3

    std::string directory = "/Calculation/conductivity_optical_nonlinear/";
       
    // regular nonlinear calculation
    if(special != 1){
      Gamma1D(NRandom, NDisorder, NMoments, process_string(dir), directory + "Gamma0" + dir);
      Gamma2D(NRandom, NDisorder, {NMoments,NMoments}, process_string(dirc1), directory + "Gamma1" + dir);
      Gamma2D(NRandom, NDisorder, {NMoments,NMoments}, process_string(dirc2), directory + "Gamma2" + dir);
      Gamma3D(NRandom, NDisorder, {NMoments,NMoments, NMoments}, process_string(dirc3), directory + "Gamma3" + dir);
    }

    // special nonlinear calculation. In this case, it's going to be HBN, which is nonlinear
    // but only has simple objects that need calculating
    if(special == 1){
      Gamma2D(NRandom, NDisorder, {NMoments,NMoments}, process_string(dirc1), directory + "Gamma1" + dir);
      Gamma2D(NRandom, NDisorder, {NMoments,NMoments}, process_string(dirc2), directory + "Gamma2" + dir);
    }
}



template void Simulation<float ,1u>::calc_condopt2();
template void Simulation<double ,1u>::calc_condopt2();
template void Simulation<long double ,1u>::calc_condopt2();
template void Simulation<std::complex<float> ,1u>::calc_condopt2();
template void Simulation<std::complex<double> ,1u>::calc_condopt2();
template void Simulation<std::complex<long double> ,1u>::calc_condopt2();
template void Simulation<float ,3u>::calc_condopt2();
template void Simulation<double ,3u>::calc_condopt2();
template void Simulation<long double ,3u>::calc_condopt2();
template void Simulation<std::complex<float> ,3u>::calc_condopt2();
template void Simulation<std::complex<double> ,3u>::calc_condopt2();
template void Simulation<std::complex<long double> ,3u>::calc_condopt2();
template void Simulation<float ,2u>::calc_condopt2();
template void Simulation<double ,2u>::calc_condopt2();
template void Simulation<long double ,2u>::calc_condopt2();
template void Simulation<std::complex<float> ,2u>::calc_condopt2();
template void Simulation<std::complex<double> ,2u>::calc_condopt2();
template void Simulation<std::complex<long double> ,2u>::calc_condopt2();

template void Simulation<float ,1u>::CondOpt2(int, int, int, int, int);
template void Simulation<double ,1u>::CondOpt2(int, int, int, int, int);
template void Simulation<long double ,1u>::CondOpt2(int, int, int, int, int);
template void Simulation<std::complex<float> ,1u>::CondOpt2(int, int, int, int, int);
template void Simulation<std::complex<double> ,1u>::CondOpt2(int, int, int, int, int);
template void Simulation<std::complex<long double> ,1u>::CondOpt2(int, int, int, int, int);
template void Simulation<float ,3u>::CondOpt2(int, int, int, int, int);
template void Simulation<double ,3u>::CondOpt2(int, int, int, int, int);
template void Simulation<long double ,3u>::CondOpt2(int, int, int, int, int);
template void Simulation<std::complex<float> ,3u>::CondOpt2(int, int, int, int, int);
template void Simulation<std::complex<double> ,3u>::CondOpt2(int, int, int, int, int);
template void Simulation<std::complex<long double> ,3u>::CondOpt2(int, int, int, int, int);
template void Simulation<float ,2u>::CondOpt2(int, int, int, int, int);
template void Simulation<double ,2u>::CondOpt2(int, int, int, int, int);
template void Simulation<long double ,2u>::CondOpt2(int, int, int, int, int);
template void Simulation<std::complex<float> ,2u>::CondOpt2(int, int, int, int, int);
template void Simulation<std::complex<double> ,2u>::CondOpt2(int, int, int, int, int);
template void Simulation<std::complex<long double> ,2u>::CondOpt2(int, int, int, int, int);

