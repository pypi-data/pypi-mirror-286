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
void Simulation<T,D>::calc_condopt(){
    debug_message("Entered Simulation::calc_condopt\n");

    // Make sure that all the threads are ready before opening any files
    // Some threads could still be inside the Simulation constructor
    // This barrier is essential
#pragma omp barrier

  int NMoments, NRandom, NDisorder, direction;
  bool local_calculate_condopt = false;
#pragma omp master
{
  auto * file = new H5::H5File(name, H5F_ACC_RDONLY);
  Global.calculate_condopt = false;
  try{
    int dummy_variable;
    get_hdf5<int>(&dummy_variable,  file, (char *)   "/Calculation/conductivity_optical/NumMoments");
    Global.calculate_condopt = true;
  } catch(H5::Exception&) {debug_message("CondOpt: no need to calculate CondOpt.\n");}
  file->close();
  delete file;
}
#pragma omp barrier
#pragma omp critical
  local_calculate_condopt = Global.calculate_condopt;

#pragma omp barrier

if(local_calculate_condopt){
#pragma omp master
      {
        std::cout << "Calculating the optical conductivity.\n";
      }
#pragma omp barrier

#pragma omp critical
{
    auto * file = new H5::H5File(name, H5F_ACC_RDONLY);

    debug_message("Optical conductivity: checking if we need to calculate Condopt.\n");
    get_hdf5<int>(&direction, file, (char *) "/Calculation/conductivity_optical/Direction");
    get_hdf5<int>(&NMoments, file, (char *)  "/Calculation/conductivity_optical/NumMoments");
    get_hdf5<int>(&NRandom, file, (char *)   "/Calculation/conductivity_optical/NumRandoms");
    get_hdf5<int>(&NDisorder, file, (char *)   "/Calculation/conductivity_optical/NumDisorder");

    file->close();
    delete file;

}
  CondOpt(NMoments, NRandom, NDisorder, direction);
  }

}
template <typename T,unsigned D>

void Simulation<T,D>::CondOpt(int NMoments, int NRandom, int NDisorder, int direction){
  std::string dir(num2str2(direction));
  std::string dirc = dir.substr(0,1)+","+dir.substr(1,2);
  Gamma1D(NRandom, NDisorder, NMoments, process_string(dir), "/Calculation/conductivity_optical/Lambda"+dir);
  Gamma2D(NRandom, NDisorder, {NMoments,NMoments}, process_string(dirc), "/Calculation/conductivity_optical/Gamma"+dir);
}



template void Simulation<float ,1u>::calc_condopt();
template void Simulation<double ,1u>::calc_condopt();
template void Simulation<long double ,1u>::calc_condopt();
template void Simulation<std::complex<float> ,1u>::calc_condopt();
template void Simulation<std::complex<double> ,1u>::calc_condopt();
template void Simulation<std::complex<long double> ,1u>::calc_condopt();
template void Simulation<float ,3u>::calc_condopt();
template void Simulation<double ,3u>::calc_condopt();
template void Simulation<long double ,3u>::calc_condopt();
template void Simulation<std::complex<float> ,3u>::calc_condopt();
template void Simulation<std::complex<double> ,3u>::calc_condopt();
template void Simulation<std::complex<long double> ,3u>::calc_condopt();
template void Simulation<float ,2u>::calc_condopt();
template void Simulation<double ,2u>::calc_condopt();
template void Simulation<long double ,2u>::calc_condopt();
template void Simulation<std::complex<float> ,2u>::calc_condopt();
template void Simulation<std::complex<double> ,2u>::calc_condopt();
template void Simulation<std::complex<long double> ,2u>::calc_condopt();

template void Simulation<float ,1u>::CondOpt(int, int, int, int);
template void Simulation<double ,1u>::CondOpt(int, int, int, int);
template void Simulation<long double ,1u>::CondOpt(int, int, int, int);
template void Simulation<std::complex<float> ,1u>::CondOpt(int, int, int, int);
template void Simulation<std::complex<double> ,1u>::CondOpt(int, int, int, int);
template void Simulation<std::complex<long double> ,1u>::CondOpt(int, int, int, int);
template void Simulation<float ,3u>::CondOpt(int, int, int, int);
template void Simulation<double ,3u>::CondOpt(int, int, int, int);
template void Simulation<long double ,3u>::CondOpt(int, int, int, int);
template void Simulation<std::complex<float> ,3u>::CondOpt(int, int, int, int);
template void Simulation<std::complex<double> ,3u>::CondOpt(int, int, int, int);
template void Simulation<std::complex<long double> ,3u>::CondOpt(int, int, int, int);
template void Simulation<float ,2u>::CondOpt(int, int, int, int);
template void Simulation<double ,2u>::CondOpt(int, int, int, int);
template void Simulation<long double ,2u>::CondOpt(int, int, int, int);
template void Simulation<std::complex<float> ,2u>::CondOpt(int, int, int, int);
template void Simulation<std::complex<double> ,2u>::CondOpt(int, int, int, int);
template void Simulation<std::complex<long double> ,2u>::CondOpt(int, int, int, int);
