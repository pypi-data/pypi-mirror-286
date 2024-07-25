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
void Simulation<T,D>::store_LMU(Eigen::Array<T, Eigen::Dynamic, Eigen::Dynamic> *gamma){
    debug_message("Entered store_lmu\n");

    auto nMoments   = static_cast<long int>(gamma->rows());
    auto nPositions = static_cast<long int>(gamma->cols());

#pragma omp master
	Global.general_gamma = Eigen::Array<T, Eigen::Dynamic, Eigen::Dynamic > :: Zero(nMoments, nPositions);
#pragma omp barrier
#pragma omp critical
	Global.general_gamma += *gamma;
#pragma omp barrier
    
#pragma omp master
{
    //std::cout << "Printing huge matrix, brb\n";
    //std::cout << Global.general_gamma << "\n" ;
    H5::H5File * file = new H5::H5File(name, H5F_ACC_RDWR);
    write_hdf5(Global.general_gamma, file, "/Calculation/ldos/lMU");
    file->close();
    delete file;
}
#pragma omp barrier    
    debug_message("Left store_lmu\n");
  }


template <typename T,unsigned D>
void Simulation<T,D>::LMU(int NDisorder, int NMoments, Eigen::Array<unsigned long, Eigen::Dynamic, 1> positions){
    debug_message("Entered Simulation::MU\n");

    typedef typename extract_value_type<T>::value_type value_type;
    Eigen::Matrix<T, 1, 2> tmp;
    auto NPositions = static_cast<int>(positions.size());
    unsigned long pos;

    KPM_Vector<T,D> kpm0(1, *this); // initial random vector
    KPM_Vector<T,D> kpm1(2, *this); // left vector that will be Chebyshev-iterated on

    // initialize the local gamma matrix and set it to 0
    Eigen::Array<T, Eigen::Dynamic, Eigen::Dynamic> gamma = Eigen::Array<T, Eigen::Dynamic, Eigen::Dynamic>::Zero(NMoments, NPositions);

    // start the kpm iteration
    Eigen::Array<long, Eigen::Dynamic, 1> average;
    average = Eigen::Array<long, Eigen::Dynamic, 1>::Zero(NPositions,1);

    for(int disorder = 0; disorder < NDisorder; disorder++){
      h.generate_disorder();
      h.generate_twists();      // Generates Random or fixed boundaries
      kpm1.initiate_phases();   //Initiates the Hopping Phases in KPM1
      
      for(int pos_index = 0; pos_index < NPositions; pos_index++){
	// Iterate over the list of positions 
	// each position is a global position. We need to find which thread contains
	// this position and the coordinates in that thread. Only THAT thread should
	// have a starting vector different from zero
	pos = positions(pos_index);
	kpm0.build_site(pos);
	
	kpm1.set_index(0);
	kpm1.v.col(0) = kpm0.v.col(0);
	kpm1.Exchange_Boundaries();
	kpm0.empty_ghosts(0);
	
	for(int n = 0; n < NMoments; n+=2)
	  {
	    kpm1.cheb_iteration(n);
	    kpm1.cheb_iteration(n+1);
	    tmp.setZero();
	    for(std::size_t ii = 0; ii < r.Sized ; ii += r.Ld[0])
	      tmp += kpm0.v.block(ii,0, r.Ld[0], 1).adjoint() * kpm1.v.block(ii, 0, r.Ld[0], 2);
	    
	    gamma(n,pos_index) += (tmp(0,0)-gamma(n,pos_index))/value_type(average(pos_index)+1);
	    gamma(n+1,pos_index) += (tmp(0,1)-gamma(n+1,pos_index))/value_type(average(pos_index)+1);
	  }
	average(pos_index)++;
      } 
    }
    store_LMU(&gamma);
    debug_message("Left Simulation::MU\n");
}

template <typename T,unsigned D>
void Simulation<T,D>::calc_LDOS(){
  debug_message("Entered Simulation::calc_LDOS\n");
  
  // Make sure that all the threads are ready before opening any files
  // Some threads could still be inside the Simulation constructor
  // This barrier is essential
#pragma omp barrier
  
  //Check if the local density of states needs to be calculated
  bool local_calculate_ldos = false;
#pragma omp master
  {
    Global.calculate_ldos = false;
    H5::H5File * file = new H5::H5File(name, H5F_ACC_RDONLY);
    try{
      int dummy_var;
      get_hdf5<int>(&dummy_var, file, (char *) "/Calculation/ldos/NumDisorder");
      Global.calculate_ldos = true;
    } catch(H5::Exception&) {
      debug_message("ldos: no need to calculate.\n");
    }
    file->close();  
    delete file;
  }
#pragma omp barrier
  
  // Now calculate it
  unsigned ldos_NumMoments;
  unsigned ldos_NumDisorder;
  Eigen::Array<unsigned long, Eigen::Dynamic, 1> ldos_Orbitals;
  Eigen::Array<unsigned long, Eigen::Dynamic, 1> ldos_Positions;
  
  local_calculate_ldos = Global.calculate_ldos;
  if(local_calculate_ldos){
#pragma omp master
    {
      std::cout << "Calculating LDoS.\n";
    }
#pragma omp barrier
    
#pragma omp critical
    {
      H5::DataSet * dataset;
      H5::DataSpace * dataspace;
      hsize_t dim[1];
      auto * file = new H5::H5File(name, H5F_ACC_RDONLY);
      dataset           = new H5::DataSet(file->openDataSet("/Calculation/ldos/Orbitals")  );
      dataspace         = new H5::DataSpace(dataset->getSpace());
      dataspace -> getSimpleExtentDims(dim, NULL);
      dataspace->close(); delete dataspace;
      dataset->close();   delete dataset;
      
      ldos_Orbitals  = Eigen::Array<unsigned long, Eigen::Dynamic, 1>::Zero(dim[0],1);
      ldos_Positions = Eigen::Array<unsigned long, Eigen::Dynamic, 1>::Zero(dim[0],1);
      
      get_hdf5<unsigned>(&ldos_NumMoments, file, (char *) "/Calculation/ldos/NumMoments");
      get_hdf5<unsigned>(&ldos_NumDisorder, file, (char *) "/Calculation/ldos/NumDisorder");
      get_hdf5<unsigned long>(ldos_Orbitals.data(), file, (char *) "/Calculation/ldos/Orbitals");
      get_hdf5<unsigned long>(ldos_Positions.data(), file, (char *) "/Calculation/ldos/FixPosition");
      file->close();  
      delete file;
    }
#pragma omp barrier
    
    Eigen::Array<unsigned long, Eigen::Dynamic, 1> total_positions;
    if(D==2){
      total_positions = ldos_Positions + ldos_Orbitals*r.Lt[0]*r.Lt[1];
    } else if(D==3){
      total_positions = ldos_Positions + ldos_Orbitals*r.Lt[0]*r.Lt[1]*r.Lt[2];
    };
    LMU(ldos_NumDisorder, ldos_NumMoments, total_positions);
  }
  debug_message("Left Simulation::calc_LDOS\n");
}


template void Simulation<float ,1u>::store_LMU(Eigen::Array<float, -1, -1>* );
template void Simulation<double ,1u>::store_LMU(Eigen::Array<double, -1, -1>* );
template void Simulation<long double ,1u>::store_LMU(Eigen::Array<long double, -1, -1>* );
template void Simulation<std::complex<float> ,1u>::store_LMU(Eigen::Array<std::complex<float>, -1, -1>* );
template void Simulation<std::complex<double> ,1u>::store_LMU(Eigen::Array<std::complex<double>, -1, -1>* );
template void Simulation<std::complex<long double> ,1u>::store_LMU(Eigen::Array<std::complex<long double>, -1, -1>* );
template void Simulation<float ,2u>::store_LMU(Eigen::Array<float, -1, -1>* );
template void Simulation<double ,2u>::store_LMU(Eigen::Array<double, -1, -1>* );
template void Simulation<long double ,2u>::store_LMU(Eigen::Array<long double, -1, -1>* );
template void Simulation<std::complex<float> ,2u>::store_LMU(Eigen::Array<std::complex<float>, -1, -1>* );
template void Simulation<std::complex<double> ,2u>::store_LMU(Eigen::Array<std::complex<double>, -1, -1>* );
template void Simulation<std::complex<long double> ,2u>::store_LMU(Eigen::Array<std::complex<long double>, -1, -1>* );
template void Simulation<float ,3u>::store_LMU(Eigen::Array<float, -1, -1>* );
template void Simulation<double ,3u>::store_LMU(Eigen::Array<double, -1, -1>* );
template void Simulation<long double ,3u>::store_LMU(Eigen::Array<long double, -1, -1>* );
template void Simulation<std::complex<float> ,3u>::store_LMU(Eigen::Array<std::complex<float>, -1, -1>* );
template void Simulation<std::complex<double> ,3u>::store_LMU(Eigen::Array<std::complex<double>, -1, -1>* );
template void Simulation<std::complex<long double> ,3u>::store_LMU(Eigen::Array<std::complex<long double>, -1, -1>* );

template void Simulation<float ,1u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);
template void Simulation<double ,1u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);
template void Simulation<long double ,1u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);
template void Simulation<std::complex<float> ,1u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);
template void Simulation<std::complex<double> ,1u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);
template void Simulation<std::complex<long double> ,1u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);
template void Simulation<float ,2u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);
template void Simulation<double ,2u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);
template void Simulation<long double ,2u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);
template void Simulation<std::complex<float> ,2u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);
template void Simulation<std::complex<double> ,2u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);
template void Simulation<std::complex<long double> ,2u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);
template void Simulation<float ,3u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);
template void Simulation<double ,3u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);
template void Simulation<long double ,3u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);
template void Simulation<std::complex<float> ,3u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);
template void Simulation<std::complex<double> ,3u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);
template void Simulation<std::complex<long double> ,3u>::LMU(int, int, Eigen::Array<unsigned long, -1, 1>);

template void Simulation<float ,1u>::calc_LDOS();
template void Simulation<double ,1u>::calc_LDOS();
template void Simulation<long double ,1u>::calc_LDOS();
template void Simulation<std::complex<float> ,1u>::calc_LDOS();
template void Simulation<std::complex<double> ,1u>::calc_LDOS();
template void Simulation<std::complex<long double> ,1u>::calc_LDOS();
template void Simulation<float ,2u>::calc_LDOS();
template void Simulation<double ,2u>::calc_LDOS();
template void Simulation<long double ,2u>::calc_LDOS();
template void Simulation<std::complex<float> ,2u>::calc_LDOS();
template void Simulation<std::complex<double> ,2u>::calc_LDOS();
template void Simulation<std::complex<long double> ,2u>::calc_LDOS();
template void Simulation<float ,3u>::calc_LDOS();
template void Simulation<double ,3u>::calc_LDOS();
template void Simulation<long double ,3u>::calc_LDOS();
template void Simulation<std::complex<float> ,3u>::calc_LDOS();
template void Simulation<std::complex<double> ,3u>::calc_LDOS();
template void Simulation<std::complex<long double> ,3u>::calc_LDOS();
