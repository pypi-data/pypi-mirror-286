/***********************************************************/
/*                                                         */
/*   Copyright (C) 2018-2022, M. Andelkovic, L. Covaci,    */
/*  A. Ferreira, S. M. Joao, J. V. Lopes, T. G. Rappoport  */
/*                                                         */
/***********************************************************/

#include <iostream>
#include <fstream>
#include <Eigen/Dense>
#include <complex>
#include <vector>
#include <string>
#include <H5Cpp.h>
#include "tools/ComplexTraits.hpp"
#include "tools/myHDF5.hpp"

#include "tools/parse_input.hpp"
#include "tools/systemInfo.hpp"
#include "spectral/dos.hpp"
#include "tools/functions.hpp"

#include "macros.hpp"
#include <cmath>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

template <typename T, unsigned DIM>
dos<T, DIM>::dos(system_info<T, DIM>& sysinfo, shell_input & vari){
    H5::Exception::dontPrint();

    systemInfo = &sysinfo;  // retrieve the information about the Hamiltonian
    variables = vari;       // retrieve the shell input

    dos_finished = false;
    MaxMoments = -1;
    isPossible = false;         // do we have all we need to calculate the density of states?
    isRequired = is_required() && variables.DOS_is_required; // check whether the DOS was requested
    if(isRequired){
        set_default_parameters();
        isPossible = fetch_parameters();
        override_parameters();      // overrides parameters with the ones from the shell input
        energies = Eigen::Matrix<T, Eigen::Dynamic, 1>::LinSpaced(NEnergies, Emin, Emax);
      if(isPossible){
          printDOS();
          calculate();
      } else {
        std::cout << "ERROR. The density of states was requested but the data "
            "needed for its computation was not found in the input .h5 file. "
            "Make sure KITEx has processed the file first. Exiting.";
        exit(1);
      }
    }
}

template <typename T, unsigned DIM>
bool dos<T, DIM>::is_required(){
    // Checks whether the DC conductivity has been requested
    // by analysing the .h5 config file. If it has been requested, 
    // some fields have to exist, such as "Direction"

    // Make sure the config filename has been initialized
    std::string name = systemInfo->filename;
    if(name == ""){
        std::cout << "ERROR: Filename uninitialized. Exiting.\n";
        exit(1);
    }

	H5::H5File file = H5::H5File(name.c_str(), H5F_ACC_RDONLY);

    std::string dirName;
    dirName = "/Calculation/dos/";
    bool result = false;
    try{
        get_hdf5(&NumMoments, &file, (char*)(dirName+"NumMoments").c_str());
        result = true;
    } catch(H5::Exception&){}


    file.close();
    return result;
}

template <typename T, unsigned DIM>
void dos<T, DIM>::set_default_parameters(){
    // Sets default values for the parameters used in the 
    // calculation of the density of stats. These are the parameters
    // that will be overwritten by the config file and the
    // shell input parameters. 

    NEnergies = 1024;           // Number of energies
    default_NEnergies = true;

    filename  = "dos.dat";      // Filename to save final result
    default_filename = true;
  
    Emax = 0.99;
    Emin = -0.99;
    default_Emin = true;
    default_Emax = true;

    kernel = "jackson";
    default_kernel = true;
    default_kernel_parameter = true;

}
	
template <typename T, unsigned DIM>
void dos<T, DIM>::override_parameters(){

    // Overrides the current parameters with the ones from the shell input.
    // These parameters are in eV or Kelvin, so they must scaled down
    // to the KPM units. This includes the temperature

    double scale = systemInfo->energy_scale;
    double shift = systemInfo->energy_shift;

    if(variables.DOS_NumEnergies != -1){
        NEnergies           = variables.DOS_NumEnergies;
        default_NEnergies   = false;
    }


    if(variables.DOS_Emin != 8888.8){
        Emin  = (variables.DOS_Emin - shift)/scale;
        default_NEnergies   = false;
    }

    if(variables.DOS_Emax != -8888.8){
        Emax  = (variables.DOS_Emax - shift)/scale;
        default_NEnergies   = false;
    }


    if(variables.DOS_NumMoments != -1){
        NumMoments         = variables.DOS_NumMoments;
        default_NumMoments = false;
        if(variables.DOS_NumMoments > MaxMoments){
          std::cout << "DOS: The number of Chebyshev moments specified"
            " cannot be larger than the number of moments calculated by KITEx."
            " Please specify a smaller number. Exiting.\n";
          exit(1);
        }
    }

    if(variables.DOS_kernel != ""){
        kernel         = variables.DOS_kernel;
        default_kernel = false;
    }

    if(kernel == "green"){
      if(variables.DOS_kernel_parameter != -8888.8){
        kernel_parameter = variables.DOS_kernel_parameter/systemInfo->energy_scale;
        default_kernel_parameter = false;
      }
    }

    if(variables.DOS_Name != ""){
        filename            = variables.DOS_Name;
        default_filename    = false;
    }
}

template <typename T, unsigned DIM>
bool dos<T, DIM>::fetch_parameters(){
	//This function reads all the data from the hdf5 file that's needed to 
    //calculate the density of states
	debug_message("Entered conductivit_dc::read.\n");


    std::string name = systemInfo->filename;
	H5::H5File file = H5::H5File(name.c_str(), H5F_ACC_RDONLY);

  
    std::string dirName;
    dirName = "/Calculation/dos/";
    
    // Fetch the number of Chebyshev Moments, temperature and number of points
    get_hdf5(&MaxMoments, &file, (char*)(dirName+"NumMoments").c_str());	
    get_hdf5(&NEnergies, &file, (char*)(dirName+"NumPoints").c_str());	
    default_NEnergies = false;

    // Check whether the matrices we're going to retrieve are complex or not
    int complex = systemInfo->isComplex;

    // Retrieve the Gamma Matrix
    bool result = false;
    std::string MatrixName = dirName + "MU";
    try{
		debug_message("Filling the MU matrix.\n");
		MU = Eigen::Array<std::complex<T>,Eigen::Dynamic,Eigen::Dynamic>::Zero(1, MaxMoments);
		
		if(complex)
			get_hdf5(MU.data(), &file, (char*)MatrixName.c_str());
		
		if(!complex){
			Eigen::Array<T,Eigen::Dynamic,Eigen::Dynamic> MUReal;
			MUReal = Eigen::Array<T,Eigen::Dynamic,Eigen::Dynamic>::Zero(1, MaxMoments);
			get_hdf5(MUReal.data(), &file, (char*)MatrixName.c_str());
			
			MU = MUReal.template cast<std::complex<T>>();
		}				

        result = true;
    } catch(H5::Exception&) {debug_message("DOS: There is no MU matrix.\n");}
    NumMoments = MaxMoments;

    // Check if the energy window has been specified
    double scale = systemInfo->energy_scale;
    double shift = systemInfo->energy_shift;
    try{
		debug_message("Fetching DoS energy window.\n");
		get_hdf5(&Emin, &file, (char*)(dirName+"dos_Emin").c_str());
		get_hdf5(&Emax, &file, (char*)(dirName+"dos_Emax").c_str());
        Emin = (Emin-shift)/scale;
        Emax = (Emax-shift)/scale;
    } catch(H5::Exception&) {debug_message("DOS: Energy window was not specified.\n");}


	file.close();
	debug_message("Left DOS::fetch_parameters.\n");
    return result;
}

template <typename T, unsigned DIM>
void dos<T, DIM>::printDOS(){
    // Prints all the information about the parameters
    
    double scale = systemInfo->energy_scale;
    double shift = systemInfo->energy_shift;
    std::string energy_range = "[" + std::to_string(Emin*scale + shift) + ", " + std::to_string(Emax*scale + shift) + "]";
    bool default_energy_limits = default_Emin && default_Emax;

    std::cout << "The density of states will be calculated with these parameters: (eV)\n"
        "   Energy range: "         << energy_range     << ((default_energy_limits)?    " (default)":"") << "\n"
        "   Number of energies: "   << NEnergies        << ((default_NEnergies)?        " (default)":"") << "\n"
        "   Filename: "             << filename         << ((default_filename)?         " (default)":"") << "\n"
        "   Number of moments: "    << NumMoments       << ((default_NumMoments)?       " (default)":"") << "\n"
        "   Kernel: "               << kernel           << ((default_kernel)?           " (default)":"") << "\n";
    if(kernel == "green"){
        std::cout << "   Kernel parameter: "     << kernel_parameter*scale << ((default_kernel_parameter)? " (default)":"") << "\n";
    }
}


template <typename T, unsigned DIM>
void dos<T, DIM>::calculate(){
  
  using namespace std::placeholders;  // for _1, _2, _3...
  
  // First perform the part of the product that only depends on the
  // chebyshev polynomial of the first kind
  GammaE = Eigen::Array<std::complex<T>, Eigen::Dynamic, Eigen::Dynamic>::Zero(NEnergies, 1);
  
  T scale = static_cast<T>(systemInfo->energy_scale);
  T mult = static_cast<T>(1.0/scale);
  T factor;
  T shift = static_cast<T>(systemInfo->energy_shift);
  
  // Choosing the kernel/exact green expansion
  
  if(kernel == "jackson"){
    for(int i = 0; i < NEnergies; i++){
      for(int m = 0; m < NumMoments; m++){
        factor = static_cast<T>(1.0/(1.0 + static_cast<T>(m==0)));
        GammaE(i) += MU(m)*delta(m,energies(i))*kernel_jackson<T>(m, NumMoments)*factor*mult;
      }
    }
  }
  
  std::complex<T> c_energy;
  if(kernel == "green"){
    for(int i = 0; i < NEnergies; i++){
      c_energy = std::complex<T>(energies(i), kernel_parameter);
      for(int m = 0; m < NumMoments; m++){
        factor = static_cast<T>(1.0/(1.0 + static_cast<T>(m==0))/M_PI);
        GammaE(i) += -MU(m)*factor*mult*green<std::complex<T>>(m, 1, c_energy).imag();
      }
    }
  }
  
  // Save the density of states to a file and find its maximum value
  std::ofstream myfile;
  myfile.open(filename);
  for(int i=0; i < NEnergies; i++){
    myfile  << energies(i)*scale + shift << " " << GammaE.real()(i) /*<< " " << GammaE.imag()(i)*/ << "\n";
  }
  myfile.close();     
  dos_finished = true;
  find_limits();      
}


template <typename T, unsigned DIM>
void dos<T,DIM>::find_limits(){
  // Check the limits of the density of states

    if(!dos_finished){
        std::cout << "Cannot estimate the limits of the density of states without first calculating it. Exiting.\n";
        exit(1);
    }

    T max = -1;
    for(int i=0; i < NEnergies; i++){
        if(GammaE(i).real() > max)
            max = GammaE(i).real();
    }
  
    T threshold = static_cast<T>(max*0.01);
    T lowest = 2, highest = -2, a, b;
    bool founda = false, foundb = false;
    for(int i = 0; i < NEnergies; i++){
        a = GammaE(i).real();
        b = GammaE(NEnergies - i - 1).real();
    
        if(a > threshold && !founda){
            lowest = energies(i);
        if(i > 0)
            lowest = energies(i-1);
        founda = true;
        }
    
        if(b > threshold && !foundb){
            highest = energies(NEnergies - i -1);
            if(i>0)
                highest = energies(NEnergies-i);
            foundb = true;
        }
    }

  systemInfo->EnergyLimitsKnown = true;
  systemInfo->minEnergy = lowest;
  systemInfo->maxEnergy = highest;
}


// Instantiations
template class dos<float, 1u>;
template class dos<float, 2u>;
template class dos<float, 3u>;

template class dos<double, 1u>;
template class dos<double, 2u>;
template class dos<double, 3u>;

template class dos<long double, 1u>;
template class dos<long double, 2u>;
template class dos<long double, 3u>;
