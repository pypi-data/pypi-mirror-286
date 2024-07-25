/***********************************************************/
/*                                                         */
/*   Copyright (C) 2018-2022, M. Andelkovic, L. Covaci,    */
/*  A. Ferreira, S. M. Joao, J. V. Lopes, T. G. Rappoport  */
/*                                                         */
/***********************************************************/

#include "Generic.hpp"
#include <Eigen/Dense>
#include <random>
#include "tools/ComplexTraits.hpp"
#include "tools/myHDF5.hpp"
#include "tools/Random.hpp"
#include "lattice/Coordinates.hpp"
#include "lattice/LatticeStructure.hpp"
template<typename T, unsigned D>
class Simulation;
#include "simulation/Global.hpp"
#include "hamiltonian/Hamiltonian.hpp"
#include "vector/KPM_VectorBasis.hpp"
#include "vector/KPM_Vector.hpp"
//#include "queue.hpp"
#include "simulation/Simulation.hpp"
#include <cmath>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

// VER o que tenho que por aqui: tile, tile_ghosts, transf_max, x, std

template <typename T>
KPM_Vector<T,3u>::KPM_Vector(int mem, Simulation<T,3u> & sim) :
  KPM_VectorBasis<T,3u>(mem, sim),
  tile{1, sim.r.Ld[0], sim.r.Ld[0] * sim.r.Ld[1] },
  transf_max{{NGHOSTS, sim.r.ld[1], sim.r.ld[2]} , { sim.r.Ld[0] , NGHOSTS, sim.r.ld[2]} , {sim.r.Ld[0], sim.r.Ld[1], NGHOSTS} },
  r(sim.r) , h(sim.h) //,  x(sim.r.Ld)
  {
    Coordinates <std::size_t, D + 1>     z(r.Ld);
    Coordinates <int, D + 1> x(r.nd), dist(r.nd);
    


    std::size_t max_0, max_1;
    
    mult_t1_ghost_cor = new   T**[r.Orb];
    
    for(unsigned io = 0; io < r.Orb; io++)
      {
        mult_t1_ghost_cor[io] = new T*[h.hr.NHoppings(io)];
        for(unsigned ib = 0; ib < h.hr.NHoppings(io); ib++)
          mult_t1_ghost_cor[io][ib] = new T[TILE];
      }

    for(unsigned d = 0; d < D; d++)
      for(unsigned b = 0; b < 2; b++)
        {
          MemIndBeg[d][b] = new std::size_t[r.Orb];
          MemIndEnd[d][b] = new std::size_t[r.Orb];
        }

    
    //   Set boundaries in x direction 
    for(unsigned edge = 0; edge < 2; edge++)
      {
        transf_bound[0][edge][0] = (r.boundary[0][edge] == true ? NGHOSTS : 0);
        transf_bound[0][edge][1] = (r.boundary[0][edge] == true ? r.ld[1] : 0);
        transf_bound[0][edge][2] = (r.boundary[0][edge] == true ? r.ld[2] : 0);
      }

    for(std::size_t io = 0; io < r.Orb; io++)
      {
        std::size_t ng = NGHOSTS, zero = 0;
        // Position of initial corner to copy to the destiny
        // From
        MemIndBeg[0][0][io] = z.set({ng,ng, ng, io}).index;   
        MemIndBeg[0][1][io] = z.set({r.Ld[0] - 2 * ng , ng, ng, io}).index;   
        // To
        MemIndEnd[0][0][io] = z.set({zero, ng, ng, io}).index;   
        MemIndEnd[0][1][io] = z.set({r.Ld[0] - ng, ng, ng, io}).index;
      }

    //   Set boundaries in y direction

    max_0 = r.ld[0] + (r.boundary[0][0] == true ? NGHOSTS : 0) + (r.boundary[0][1] == true ? NGHOSTS : 0) ;        
    for(unsigned edge = 0; edge < 2; edge++)
      {        
        transf_bound[1][edge][0] = (r.boundary[1][edge] == true ? max_0 : 0);
        transf_bound[1][edge][1]  = (r.boundary[1][edge] == true ? NGHOSTS : 0);
        transf_bound[1][edge][2] = (r.boundary[1][edge] == true ? r.ld[2] : 0);
      }
    
    for(std::size_t io = 0; io < r.Orb; io++)
      {
        std::size_t ng = NGHOSTS, zero = 0;
        std::size_t minx = (r.boundary[0][0] == true ? zero : NGHOSTS);
        // X is periodic in left direction         
        MemIndBeg[1][0][io] = z.set({minx, ng, ng, io}).index;   
        MemIndBeg[1][1][io] = z.set({minx, r.Ld[1] - 2*ng, ng, io}).index;   
        // Position of initial corner to copy to the destiny 
        MemIndEnd[1][0][io] = z.set({minx, zero, ng, io}).index;   
        MemIndEnd[1][1][io] = z.set({minx, r.Ld[1] - ng, ng, io}).index;
      }    

    //   Set boundaries in z direction
    max_0 = r.ld[0] + (r.boundary[0][0] == true ? NGHOSTS : 0) + (r.boundary[0][1] == true ? NGHOSTS : 0); 
    max_1 = r.ld[1] + (r.boundary[1][0] == true ? NGHOSTS : 0) + (r.boundary[1][1] == true ? NGHOSTS : 0);

    for(unsigned edge = 0; edge < 2; edge++)
      {
        transf_bound[2][edge][0] = (r.boundary[2][edge] == true ? max_0 : 0);
        transf_bound[2][edge][1] = (r.boundary[2][edge] == true ? max_1 : 0);
        transf_bound[2][edge][2] = (r.boundary[2][edge] == true ? NGHOSTS : 0);
      }

    for(std::size_t io = 0; io < r.Orb; io++)
      {
        std::size_t ng = NGHOSTS, zero = 0;
        std::size_t minx = (r.boundary[0][0] == true ? zero : NGHOSTS);
        std::size_t miny = (r.boundary[1][0] == true ? zero : NGHOSTS);
        
        MemIndBeg[2][0][io] = z.set({minx, miny, ng, io}).index;
        MemIndBeg[2][1][io] = z.set({minx, miny, r.Ld[2] - 2*ng, io}).index;   
        // Position of initial corner to copy to the destiny 
        MemIndEnd[2][0][io] = z.set({minx, miny, zero, io}).index;   
        MemIndEnd[2][1][io] = z.set({minx, miny, r.Ld[2] - ng, io}).index;                
      }    

    for(unsigned d = 0 ; d < D; d++)
      for(unsigned b  = 0 ; b < 2; b++)
        {
          dist.set({0,0,0,0});
          dist.coord[d] = int(b) * 2 - 1;
          block[d][b] = x.set_coord( int(r.thread_id) ).add(dist).index;
        }

    // JPPP Calcular os vectores das fases devido às condicoes fronteira
    for(unsigned i = 0; i < D; i ++)
      for(unsigned j = 0; j < 3; j ++)
	Fact_Bnd[i][j] = new T[r.Ld[i]];
    
    initiate_vector();
  }

template <typename T>
KPM_Vector <T, 3u>::~KPM_Vector(void) {
  
  
  for(unsigned io = 0; io < r.Orb;io++)
    {
      for(unsigned ib = 0; ib < h.hr.NHoppings(io); ib++)
        delete mult_t1_ghost_cor[io][ib];
      delete mult_t1_ghost_cor[io];
    }  
  delete mult_t1_ghost_cor;
  
  for(unsigned d = 0; d < D; d++)
    for(unsigned b = 0; b < 2; b++)
      {
        delete MemIndBeg[d][b];
        delete MemIndEnd[d][b];
      }  
}


template <typename T>
void KPM_Vector <T, 3u>::initiate_vector(){  
  index = 0;

  // Check if the SEED variable is set to deterministic
  char *env;
  std::string seed("");
  env = getenv("SEED");
  if(env != NULL) seed = std::string(env);

    
  // Set all numbers to ones
  if(seed=="ones"){
      Coordinates<std::size_t, 4> x(r.Ld);
      for(std::size_t io = 0; io < r.Orb; io++)
        for(std::size_t i2 = NGHOSTS; i2 < r.Ld[2] - NGHOSTS; i2++)
          for(std::size_t i1 = NGHOSTS; i1 < r.Ld[1] - NGHOSTS; i1++)
            for(std::size_t i0 = NGHOSTS; i0 < r.Ld[0] - NGHOSTS; i0++)
              v(x.set({i0,i1,i2,io}).index, index) = 1.0/static_cast<value_type>(sqrt(value_type(r.Sizet - r.SizetVacancies)));

  // Proceed normally
  } else {
      Coordinates<std::size_t, 4> x(r.Ld);
      for(std::size_t io = 0; io < r.Orb; io++)
        for(std::size_t i2 = NGHOSTS; i2 < r.Ld[2] - NGHOSTS; i2++)
          for(std::size_t i1 = NGHOSTS; i1 < r.Ld[1] - NGHOSTS; i1++)
            for(std::size_t i0 = NGHOSTS; i0 < r.Ld[0] - NGHOSTS; i0++)
              v(x.set({i0,i1,i2,io}).index, index) = simul.rnd.init()/static_cast<value_type>(sqrt(value_type(r.Sizet - r.SizetVacancies)));
  }
  
  // Set to zero the places where there are vacancies
  for(unsigned i = 0; i < r.NStr; i++){
      auto & vv = h.hV.position.at(i); 
      for(unsigned j = 0; j < vv.size(); j++)
        v(vv.at(j), index ) = 0. ;
  }

  // Initiate the phases for the twisted boundary conditions
  initiate_phases();
}

template <typename T>
void KPM_Vector <T, 3>::initiate_phases() {
  // JPPP Calcular os vectores das fases devido às condicoes fronteira
  Coordinates<std::size_t, 4> x(r.Ld), z(r.Lt);
#pragma omp critical
  {
    for(unsigned i = NGHOSTS; i < r.Ld[0] - NGHOSTS; i++)
      {
	x.set({i, 0, 0, 0});
	r.convertCoordinates(z,x);
	Fact_Bnd[0][2][x.coord[0]] = exp(ComplexTraits<T>::assign_value(0.0,-1.0*(h.BoundTwist[0] * int((int(z.coord[0]) + 1)/r.Lt[0]))));
	Fact_Bnd[0][1][x.coord[0]] = ComplexTraits<T>::assign_value(1.0,0.0);
	Fact_Bnd[0][0][x.coord[0]] = exp(ComplexTraits<T>::assign_value(0.0,h.BoundTwist[0] * int((int(r.Lt[0] - z.coord[0]))/r.Lt[0])));
      }
    for(unsigned i = NGHOSTS; i < r.Ld[1] - NGHOSTS; i++)
      {
	x.set({0, i, 0, 0});
	r.convertCoordinates(z,x);
	Fact_Bnd[1][2][x.coord[1]] = exp(ComplexTraits<T>::assign_value(0.0,-1.0*(h.BoundTwist[1] * int((int(z.coord[1]) + 1)/r.Lt[1]))));
	Fact_Bnd[1][1][x.coord[1]] = ComplexTraits<T>::assign_value(1.0,0.0);
	Fact_Bnd[1][0][x.coord[1]] = exp(ComplexTraits<T>::assign_value(0.0,h.BoundTwist[1] * int((int(r.Lt[1] - z.coord[1]))/r.Lt[1])));
      }
    for(unsigned i = NGHOSTS; i < r.Ld[2] - NGHOSTS; i++)
      {
	x.set({0, 0, i, 0});
	r.convertCoordinates(z,x);
	Fact_Bnd[2][2][x.coord[2]] = exp(ComplexTraits<T>::assign_value(0.0,-1.0*(h.BoundTwist[2] * int((int(z.coord[2]) + 1)/r.Lt[2]))));
	Fact_Bnd[2][1][x.coord[2]] = ComplexTraits<T>::assign_value(1.0,0.0);
	Fact_Bnd[2][0][x.coord[2]] = exp(ComplexTraits<T>::assign_value(0.0,h.BoundTwist[2] * int((int(r.Lt[2] - z.coord[2]))/r.Lt[2])));
      }
  }
}

template <typename T>
T KPM_Vector <T, 3>::get_point()
{
  T point;

  if(r.thread_id == 0)
    {
      Coordinates<std::size_t, 4> x(r.Ld);
      std::size_t indice = x.set({std::size_t(r.Ld[0]/2), std::size_t(r.Ld[1]/2), std::size_t(r.Ld[2]/2), std::size_t(0)}).index;
      point = v(indice,index);
    }
  else
    point = assign_value(0,0);

  return point;
}


template <typename T>
void KPM_Vector <T, 3>::build_wave_packet(Eigen::Matrix<double,Eigen::Dynamic,Eigen::Dynamic> & k, Eigen::Matrix<T,Eigen::Dynamic,Eigen::Dynamic> & psi0, double & sigma,
                                          Eigen::Matrix<double,1,2> & vb)
{
  index = 0;
  Coordinates<std::size_t, 4> x(r.Ld), z(r.Lt);
  Eigen::Matrix<T,Eigen::Dynamic,Eigen::Dynamic>  sum(r.Orb, 1);
  Eigen::Map<Eigen::Matrix<std::size_t,3, 1>> vv(z.coord);
  Eigen::Matrix<double, 1, 3> va;
  Eigen::Matrix<double, Eigen::Dynamic,Eigen::Dynamic> phase(1, psi0.cols());
  T soma = assign_value(0,0);
  auto bbs = r.rLat.inverse(); // each row is a bi / 2*M_PI 
  auto vOrb = bbs * r.rOrb;    // each columns is a vector in a1 basis
    

//  vb(0,0) = r.Lt[0]/2;
//  vb(0,1) = r.Lt[1]/2;
//  vb(0,2) = r.Lt[2]/2;
    
  double a00 = r.rLat.col(0).transpose()*r.rLat.col(0);
  double a11 = r.rLat.col(1).transpose()*r.rLat.col(1);
  double a22 = r.rLat.col(2).transpose()*r.rLat.col(2);
  double a01 = r.rLat.col(0).transpose()*r.rLat.col(1);
  double a02 = r.rLat.col(0).transpose()*r.rLat.col(2);
  double a12 = r.rLat.col(1).transpose()*r.rLat.col(2);
  
#pragma omp master 
  {
    simul.Global.mu = Eigen::Matrix<T,Eigen::Dynamic,Eigen::Dynamic>(psi0.cols(), 1);
    for(int ik = 0; ik < psi0.cols(); ik++)
      simul.Global.mu(ik, 0) = assign_value( simul.rnd.get(), 0 );
  }
#pragma omp barrier
  
#pragma omp critical
  for(int ik = 0; ik < psi0.cols(); ik++)
    phase(0,ik)  = std::real(simul.Global.mu(ik, 0)) ;
#pragma omp barrier
  for(std::size_t i2 = NGHOSTS; i2 < r.Ld[2] - NGHOSTS; i2++)
    for(std::size_t i1 = NGHOSTS; i1 < r.Ld[1] - NGHOSTS; i1++)
      for(std::size_t i0 = NGHOSTS; i0 < r.Ld[0] - NGHOSTS; i0++)
        {
          x.set({i0,i1,std::size_t(0)});
          r.convertCoordinates(z,x);
          double n2 = (double(z.coord[2]) - double(vb(0,2)))/sigma;
          double n1 = (double(z.coord[1]) - double(vb(0,1)))/sigma;
          double n0 = (double(z.coord[0]) - double(vb(0,0)))/sigma;
          double gauss = n0*n0 * a00 + n1*n1 * a11 + n2*n2*a22 + 2*n0*n1*a01 + 2*n0*n2*a02 + 2*n1*n2*a12;
          sum.setZero();
          va = vv.cast<double>().transpose();
            
          for(int ik = 0; ik < psi0.cols(); ik++)
            {
              for(unsigned io = 0; io < r.Orb; io++)
                {
                  double xx = (va  + vOrb.col(io).transpose() ) * k.col(ik);
                  sum(io, 0) += psi0(io,ik) * exp(assign_value(-0.5*gauss,  2.*M_PI * (xx + 0.*phase(0,ik) )));
                }
            }
            
          for(std::size_t io = 0; io < r.Orb; io++)
            {
              x.set({i0,i1,io});
              v(x.index, 0) = sum(io,0);
              soma += assign_value( std::real( sum(io,0) * std::conj(sum(io,0)) ), 0);
            }
        }
  
#pragma omp master
  simul.Global.soma = assign_value(0,0);
#pragma omp barrier
#pragma omp critical
  simul.Global.soma += soma;
#pragma omp barrier
  soma = simul.Global.soma;
  value_type soma2 = sqrt(std::real(soma));
  
  for(std::size_t io = 0; io < r.Orb; io++)
    for(std::size_t i2 = NGHOSTS; i2 < r.Ld[2] - NGHOSTS; i2++)
      for(std::size_t i1 = NGHOSTS; i1 < r.Ld[1] - NGHOSTS; i1++)
        for(std::size_t i0 = NGHOSTS; i0 < r.Ld[0] - NGHOSTS; i0++)
          {
            x.set({i0,i1,i2,io});
            v(x.index, 0) /= soma2;
          }
}




template <typename T>
void KPM_Vector <T, 3>::test_boundaries_system() {
  
  /*
    This  function tests if the boudaries exchange are well implemented 
  */
 
  Coordinates<std::size_t, 4> z(r.Lt);
  Coordinates<std::size_t, 4> x(r.Ld);
  
  for(std::size_t  io = 0; io < (std::size_t) r.Ld[3]; io++)
    for(std::size_t i2 = 0; i2 < (std::size_t) r.Ld[2] ; i2++)
      for(std::size_t i1 = NGHOSTS; i1 < (std::size_t) r.Ld[1] - NGHOSTS ; i1++)
        for(std::size_t i0 = NGHOSTS; i0 < (std::size_t) r.Ld[0] - NGHOSTS ; i0++)
          {
            r.convertCoordinates(z, x.set({i0,i1,i2,io}) );
            v(x.set({i0,i1,io}).index, 0) = aux_wr(z.index);
          }
  
  Exchange_Boundaries();
#pragma omp barrier
  
#pragma omp critical
  {
    for(std::size_t  io = 0; io < (std::size_t) r.Ld[3]; io++)
      for(std::size_t i2 = 0; i2 < (std::size_t) r.Ld[2] ; i2++)
        for(std::size_t i1 = 0; i1 < (std::size_t) r.Ld[1] ; i1++)
          for(std::size_t i0 = 0; i0 < (std::size_t) r.Ld[0]; i0++)
            {
              r.convertCoordinates(z, x.set({i0,i1,i2,io}) );
              T val = aux_wr(z.index);
              
              if( aux_test(v(x.index , 0), val ) )
                {
                  std::cout << "Problems---->" << v(x.index , 0) << " " << val << " ";
                  std::cout << "\t wrong " << std::real(v(x.index , 0)) << " " << z.index << " " << x.index << "\t\t";
                  x.print();
                };
            }
  }
  std::cout << "Thread : " << r.thread_id << std::endl;
#pragma omp barrier
  exit(1);
  
}




template <typename T>
void KPM_Vector <T, 3>::empty_ghosts(int mem_index) {

  
  /* This function takes the kpm vector that's being used, 'v' and sets to zero the part corresponding
   * to the ghosts, that is, the part of the vector that actually belongs to a different thread.
   * This is done so that when we take the dot product 'v' with another vector only terms pertraining 
   * to the current thread are considered.
   * */
  
  Coordinates<long, 4u> x(r.Ld);
  const long NGHL = NGHOSTS;
  
  // There are four sides, so set the ghosts in each side to zero individually.
  // Remember that the size of the ghost boundaries depends on NGHOSTS.

  // perpendicular to x axis
  
  for(long  io = 0; io < static_cast<long>(r.Ld[3]); io++)
    for(long i2 = 0; i2 < static_cast<long>(r.Ld[2]); i2++)
      for(long i1 = 0; i1 <  static_cast<long>(r.Ld[1]); i1++)
        for(long i0 = 0; i0 < NGHL; i0++)
          {
            v(x.set({i0,i1,i2,io}).index, mem_index) *= 0;
            v(x.set({static_cast<long>(r.Ld[0]) - 1 - i0, i1, i2, io}).index, mem_index) *= 0;
          }

  // perpendicular to y axis
  
  for(long  io = 0; io < static_cast<long>(r.Ld[3]); io++)
    for(long i2 = 0; i2 < static_cast<long>(r.Ld[2]); i2++)
      for(long i1 = 0; i1 < NGHL; i1++)
        for(long i0 = 0; i0 < static_cast<long>(r.Ld[0]); i0++)
          {
            v(x.set({i0,i1,i2,io}).index, mem_index) *= 0;
            v(x.set({i0,static_cast<long>(r.Ld[1]) - 1 -  i1, i2, io}).index, mem_index) *= 0;
          }
  
  // perpendicular to y axis
  
  for(long  io = 0; io < static_cast<long>(r.Ld[3]); io++)
    for(long i2 = 0; i2 < NGHL; i2++)
      for(long i1 = 0; i1 < static_cast<long>(r.Ld[1]); i1++)
        for(long i0 = 0; i0 <  static_cast<long>(r.Ld[0]); i0++)
          {
            v(x.set({i0,i1,i2,io}).index, mem_index) *= 0;
            v(x.set({i0,i1,static_cast<long>(r.Ld[2]) - 1 - i2, io}).index, mem_index) *= 0;
          }
}


template <typename T>
void KPM_Vector <T, 3>::measure_wave_packet(T * bra, T * ket, T * results)  
{
  
  Coordinates<std::size_t,4> ad(r.Ld), at(r.Lt);
  ad.set({std::size_t(NGHOSTS), std::size_t(NGHOSTS), std::size_t(NGHOSTS), std::size_t(0)});
  r.convertCoordinates(at,ad);
  for(unsigned i = 0; i < 2*D; i++)
    results[i] *= 0.;
  
  for(unsigned io = 0; io < r.Orb; io++)
    {
      auto deltax = static_cast<value_type>(r.rOrb(0,io));
      auto deltay = static_cast<value_type>(r.rOrb(1,io));
      auto deltaz = static_cast<value_type>(r.rOrb(2,io));
      
      for(unsigned i2 = 0; i2 < r.ld[2]; i2++)
        for(unsigned i1 = 0; i1 < r.ld[1]; i1++)
          {
            std::size_t ind = ad.set({std::size_t(NGHOSTS),std::size_t(NGHOSTS + i1), std::size_t(i2 + NGHOSTS), std::size_t(io)}).index;
            auto z0 = static_cast<value_type>(at.coord[0] +  0);
            auto z1 = static_cast<value_type>(at.coord[1] + i1);
            auto z2 = static_cast<value_type>(at.coord[2] + i2);
            
            auto xt = static_cast<value_type>(z0*r.rLat(0,0) + z1 * r.rLat(0,1) + z2 * r.rLat(0,2) + deltax);
            auto yt = static_cast<value_type>(z0*r.rLat(1,0) + z1 * r.rLat(1,1) + z2 * r.rLat(1,2) + deltay);
            auto zt = static_cast<value_type>(z0*r.rLat(0,0) + z1 * r.rLat(2,1) + z2 * r.rLat(2,2) + deltaz);
            
            
            T xl1 = assign_value(0., 0.);
            T xl2 = assign_value(0., 0.);
            T yl1 = assign_value(0., 0.);
            T yl2 = assign_value(0., 0.);
            T zl1 = assign_value(0., 0.);
            T zl2 = assign_value(0., 0.);
	    
            for(unsigned i0 = 0; i0 < r.ld[0]; i0++)
              {
                std::size_t j0 = ind + i0;
                auto x = static_cast<value_type>(xt + i0 * r.rLat(0,0));
                auto y = static_cast<value_type>(yt + i0 * r.rLat(1,0));
                auto z = static_cast<value_type>(zt + i0 * r.rLat(2,0));
                
                T p = myconj(*(bra + j0)) * (*(ket + j0));
                xl1 += p * x;
                xl2 += p * x * x;
                yl1 += p * y;
                yl2 += p * y * y;
                zl1 += p * z;
                zl2 += p * z * z;
              }
            
            results[0] += xl1;
            results[1] += xl2;
            results[2] += yl1;
            results[3] += yl2;
            results[4] += zl1;
            results[5] += zl2;
          }
    }
  // Periodic component of the Hamiltonian + Anderson disorder
  
}



// Structural disorder contribution - iterate over the disorder models
template <typename T>
void KPM_Vector <T, 3>::Exchange_Boundaries() {
  /*
    I have four boundaries to exchange with the other threads.
    First I will copy the lines along the a[1] direction to a consecutive shared vector
  */
  
#pragma omp barrier    
  Coordinates<std::size_t,4u> x(r.Ld), z(r.Lt);
  T  *phi = v.col(index).data();
  
   
  for(unsigned d = 0; d < 3; d++)
    {
      std::size_t BSize = r.Orb * transf_max[d][0] *transf_max[d][1] * transf_max[d][2];
      
      T * ghosts_left = & simul.ghosts[0];
      T * ghosts_right = & simul.ghosts[BSize];

      for(std::size_t io = 0; io < r.Orb; io++)
        {
          std::size_t il = MemIndBeg[d][0][io];
          std::size_t ir = MemIndBeg[d][1][io];
          std::size_t irefPakLeft  = io *  transf_bound[d][0][2] * transf_bound[d][0][1] * transf_bound[d][0][0];
          std::size_t irefPakRight = io *  transf_bound[d][1][2] * transf_bound[d][1][1] * transf_bound[d][1][0];
          
          // Copy Left Edge
          
          for(std::size_t i2 = 0; i2 < transf_bound[d][0][2]; i2++)
            for(std::size_t i1 = 0; i1 < transf_bound[d][0][1]; i1++)
              {
                std::size_t iref = il + i2 * tile[2] + i1 * tile[1];
                for(std::size_t i0 = 0; i0 < transf_bound[d][0][0]; i0++)
                  ghosts_left[irefPakLeft + i0] = phi[iref + i0];
                irefPakLeft += transf_bound[d][0][0];
              }
          
          // Copy Right
          
          for(std::size_t i2 = 0; i2 < transf_bound[d][1][2]; i2++)
            for(std::size_t i1 = 0; i1 < transf_bound[d][1][1]; i1++)
              {
                std::size_t iref = ir + i2 * tile[2] + i1 * tile[1];
                for(std::size_t i0 = 0; i0 < transf_bound[d][1][0]; i0++)
                  ghosts_right[irefPakRight + i0] = phi[iref + i0];
                irefPakRight += transf_bound[d][1][0];
              }
          
	}
      // Copy the boundaries to the shared memory
      std::copy( ghosts_left, ghosts_left + 2*BSize, simul.Global.ghosts.begin() + 2*BSize * r.thread_id );	  
#pragma omp barrier
      auto neigh_left = simul.Global.ghosts.begin() + 2 * block[d][0] * BSize;
      auto neigh_right  = simul.Global.ghosts.begin() + 2 * block[d][1] * BSize;
      std::copy(neigh_right,         neigh_right + BSize , ghosts_right );     // From the left to the right
      std::copy(neigh_left + BSize,  neigh_left + 2*BSize, ghosts_left  )  ;   // From the right to the left
      
#pragma omp barrier	
      for(std::size_t io = 0; io < r.Orb; io++)
        {
          std::size_t il = MemIndEnd[d][0][io];
          std::size_t ir = MemIndEnd[d][1][io];
          std::size_t irefPakLeft  = io *  transf_bound[d][0][2] * transf_bound[d][0][1] * transf_bound[d][0][0];
          std::size_t irefPakRight = io *  transf_bound[d][1][2] * transf_bound[d][1][1] * transf_bound[d][1][0];
          
          
          // Copy Left Edge
          
          for(std::size_t i2 = 0; i2 < transf_bound[d][0][2]; i2++)
            for(std::size_t i1 = 0; i1 < transf_bound[d][0][1]; i1++)
              {
                std::size_t iref = il + i2 * tile[2] + i1 * tile[1];
                for(std::size_t i0 = 0; i0 < transf_bound[d][0][0]; i0++)
                  phi[iref + i0] = ghosts_left[irefPakLeft + i0];
                irefPakLeft += transf_bound[d][0][0];
              }
          
          // Copy Right
          
          for(std::size_t i2 = 0; i2 < transf_bound[d][1][2]; i2++)
            for(std::size_t i1 = 0; i1 < transf_bound[d][1][1]; i1++)
              {
                std::size_t iref = ir + i2 * tile[2] + i1 * tile[1];
                for(std::size_t i0 = 0; i0 < transf_bound[d][1][0]; i0++)
                  phi[iref+i0] = ghosts_right[irefPakRight + i0];
                irefPakRight += transf_bound[d][1][0];
              }
        }
    }

} 

template <typename T>
void inline KPM_Vector <T, 3>::mult_regular_hoppings(const  std::size_t & ind_i, const  std::size_t & io){
    /* Perform the KPM iteration for the regular part of the Hamiltonian, that is, the translation-invariant part 
     * */

  std::size_t count;
  const std::size_t ind_f = ind_i + TILE * tile[2];
  std::size_t rr[3], hop[3], x, y, z; // Variables for TBC

  // Iterate over the hoppings
  for(unsigned ib = 0; ib < h.hr.NHoppings(io); ib++){
      rr[0] = (ind_i % r.Ld[0]);
      rr[1] = (ind_i % (r.Ld[0] * r.Ld[1]) )/(r.Ld[0]);
      rr[2] = (ind_i % (r.Ld[0] * r.Ld[1] * r.Ld[2]) )/(r.Ld[0]*r.Ld[1]);
	
      const std::ptrdiff_t d1 = h.hr.distance(ib, io);

      // Determine the Supercell Jumps
      const std::size_t i_f = ind_i + d1;
      hop[0] = (i_f % r.Ld[0] ) - rr[0] +1 ;
      hop[1] = (i_f % (r.Ld[0] * r.Ld[1]) )/(r.Ld[0]) - rr[1] + 1;
      hop[2] = (i_f % (r.Ld[0] * r.Ld[1] * r.Ld[2]) )/(r.Ld[0]*r.Ld[1]) - rr[2] + 1;
      
      count = 0;
      z = 0;

      // Iterate over the slowest coordinate (z)
      for( std::size_t j2 = ind_i; j2 < ind_f; j2 += tile[2] ) {
          const T t1 = mult_t1_ghost_cor[io][ib][count++] * Fact_Bnd[2][hop[2]][rr[2]+z];
          const std::size_t std = tile[1], j2M = j2 + std * TILE;
	      y = 0;

          // Iterate over the middle coordinate (y)
          for(std::size_t j1 = j2; j1 < j2M; j1 += std ){
              x = 0;

              // Iterate over the quick coordinate (x)
              for(std::size_t j0 = j1; j0 < j1 + TILE ; j0++){
                phi0[j0] += t1 * phiM1[j0 + d1] * Fact_Bnd[1][hop[1]][rr[1]+y] * Fact_Bnd[0][hop[0]][rr[0]+x];
                x++;
              };
	          y++;
	       };
	       z++;
	  };
    } 
}

template <typename T>
template < unsigned MULT> 
void inline KPM_Vector <T, 3>::mult_local_disorder(const  std::size_t & ind_i, const  std::size_t & io)
{
  
  const std::size_t ind_f = ind_i + TILE * tile[2];
  const std::ptrdiff_t dd = (h.Anderson_orb_address[io] - std::ptrdiff_t(io))*r.Nd;
  // Anderson disorder
  if( h.Anderson_orb_address[io] >= 0)
    {
      for(std::size_t j2 = ind_i; j2 < ind_f; j2 += tile[2] )
        for(std::size_t j1 = j2; j1 < j2 + tile[1] * TILE; j1 += tile[1] )
          for(std::size_t j0 = j1; j0 < j1 + TILE ; j0++)
            phi0[j0] += value_type(MULT + 1) * phiM1[j0] * h.U_Anderson.at(j0 + dd);
    }
  else if (h.Anderson_orb_address[io] == - 1)
    {
      for(std::size_t j2 = ind_i; j2 < ind_f; j2 += tile[2] )
        for(std::size_t j1 = j2; j1 < j2 + tile[1] * TILE; j1 += tile[1] )
          for(std::size_t j0 = j1; j0 < j1 + TILE ; j0++)
            phi0[j0] += value_type(MULT + 1) * phiM1[j0] * h.U_Orbital.at(io);
    }

  // Custom local disorder
  if(h.is_custom_local_set){
      for(std::size_t j2 = ind_i; j2 < ind_f; j2 += tile[2] )
        for(std::size_t j1 = j2; j1 < j2 + tile[1] * TILE; j1 += tile[1] )
          for(std::size_t j0 = j1; j0 < j1 + TILE ; j0++)
            phi0[j0] += value_type(MULT + 1) * phiM1[j0] * h.custom_local(j0);
  }
  
}


template <typename T>
template < unsigned MULT> 
void KPM_Vector <T, 3u>::initiate_stride(std::size_t & istr)
{
  
  const std::size_t Delta_2 = tile[2] * TILE, Delta_1 = tile[1] * TILE;
  Coordinates<std::size_t, 4u> rStr(r.lStr);
  Coordinates<std::size_t, 4u> rLd(r.Ld);
  // Periodic component of the Hamiltonian + Anderson disorder
  rStr.set_coord(istr);
  std::size_t i0 = rStr.coord[0] * TILE + NGHOSTS;
  std::size_t i1 = rStr.coord[1] * TILE + NGHOSTS;
  std::size_t i2 = rStr.coord[2] * TILE + NGHOSTS;
  
  for(std::size_t io = 0; io < r.Orb; io++)
    {
      const std::size_t ind_i = rLd.set({i0,i1,i2,io}).index;
      for(std::size_t j2 = ind_i; j2 < ind_i + Delta_2; j2 += tile[2] )
        for(std::size_t j1 = j2; j1 < j2 + Delta_1; j1 += tile[1] )
          for(std::size_t j0 = j1; j0 < j1 + TILE ; j0++)
            phi0[j0] = - value_type(MULT) * phiM2[j0];
    }
  
}


template <typename T>
template < unsigned MULT,bool VELOCITY> 
void KPM_Vector <T, 3>::build_regular_phases(int i2min, unsigned axis) {

  Coordinates<std::ptrdiff_t, D + 1>  global(r.Lt);
  Coordinates<std::ptrdiff_t, D + 1>  local1(r.Ld);
  Coordinates<std::ptrdiff_t, D + 1>     b3(r.lB3);    
  Eigen::Map<Eigen::Matrix<std::ptrdiff_t,D, 1>> vee(b3.coord); // Column vector
  
  
  for(unsigned io = 0; io < r.Orb; io++)
    {
      r.convertCoordinates(global, local1.set({0,0,i2min,io}));      
      
      for(unsigned ib = 0; ib < h.hr.NHoppings(io); ib++)
        {
          T tt  = value_type(MULT + 1) * h.hr.hopping(ib, io);
          b3.set_coord(h.hr.dist(ib,io)); //  hr.dist has the coordinated in 3 Basis of relative hopping
          vee.array() -= 1;
          
          if (VELOCITY)
            tt  *=  h.hr.v.at(axis)(ib,io);
          
          for(std::size_t i2 = 0; i2 < TILE; i2++ )
            {
              auto phase = static_cast<value_type>(vee(0) * (global.coord[2] + int(i2)) * r.ghost_pot(0,D - 2));
              mult_t1_ghost_cor[io][ib][i2] =  tt * multEiphase(phase);
            }
        }
    }  
}


template <typename T>
template <unsigned MULT, bool VELOCITY>
void KPM_Vector <T, 3>::KPM_MOTOR(KPM_Vector<T,3> *kpm_final, unsigned axis)
{
  std::size_t i0, i1, i2;
  Coordinates<std::size_t, D + 1> x(r.Ld);
  phi0 = kpm_final->v.col(kpm_final->index).data();
  phiM1 = v.col( (memory - 1 + index) % memory ).data();
  phiM2 = v.col( (memory - 2 + index) % memory ).data();
  
  // Initialize tiles that have deffects connecting elements of a previous tile
  for(auto istr = h.cross_mozaic_indexes.begin(); istr != h.cross_mozaic_indexes.end() ; istr++)
    initiate_stride<MULT>(*istr);
  
  // Iterate over tiles first
  for( i2 = NGHOSTS; i2 < r.Ld[2] - NGHOSTS; i2 += TILE  ){
      build_regular_phases<MULT,VELOCITY>(static_cast<int>(i2), axis);
      for( i1 = NGHOSTS; i1 < r.Ld[1] - NGHOSTS; i1 += TILE  )
        for( i0 = NGHOSTS; i0 < r.Ld[0] - NGHOSTS; i0 += TILE ){
            
            std::size_t istr = ((i2 - NGHOSTS) / TILE * r.lStr[1] + (i1 - NGHOSTS) / TILE) * r.lStr[0] + (i0 - NGHOSTS) / TILE;
            if(h.cross_mozaic.at(istr))
              initiate_stride<MULT>(istr);

            // Iterate over the orbitals
            for(std::size_t io = 0; io < r.Orb; io++){
                const std::size_t ip = io * x.basis[3];
                const std::size_t j0 = ip + i0 + i1 * tile[1] + i2 * tile[2];
		
                // Local Energy
                if(!VELOCITY) mult_local_disorder<MULT>(j0, io);
		
                // Hoppings
                mult_regular_hoppings(j0, io);
             }
            
            KPM_VectorBasis<T,3u>::template multiply_defect<MULT, VELOCITY>(istr, phi0, phiM1, axis);
            
            // Empty the vacancies in the tile
            auto & hV = h.hV.position.at(istr);
            for(auto k = hV.begin(); k != hV.end(); k++)
              phi0[*k] = 0.;

        }
    }

  for(auto vc =  h.hV.vacancies_with_defects.begin(); vc != h.hV.vacancies_with_defects.end(); vc++)
    phi0[*vc] = 0.;
    
  /* 
     Broken Imputirities:
     The bulk domain will receive contributions from the broken defects 
     located on the neighbour domains.
     We already subtract the vacancies from these contributions 
  */

  for(auto id = h.hd.begin(); id != h.hd.end(); id++)
    id->template multiply_broken_defect<MULT,VELOCITY>(phi0, phiM1,axis);
	  
  // These four lines pertrain only to the magnetic field
  Exchange_Boundaries();
  
}


template <typename T>
void KPM_Vector <T, 3>::build_site(unsigned long pos){
  // Builds an initial vector which is zero everywhere except
  // for a single site, where it is one
  
  Coordinates<unsigned long, D + 1> thread_coords(r.ld);
  Coordinates<unsigned long, D + 1> thread_coords_gh(r.Ld);
  Coordinates<unsigned long, D + 1> thread(r.nd);
  Coordinates<unsigned long, D + 1> total_coords(r.Lt);
  bool correct_thread;
  unsigned long T_thread[D + 1]; // index of the thread
  unsigned long x_thread[D + 1]; // position within the thread
  
  index = 0;
#pragma omp critical
  {
    total_coords.set_coord(pos);
    for(unsigned d = 0; d < D; d++)
      {
	T_thread[d] = total_coords.coord[d]/r.ld[d];
	x_thread[d] = total_coords.coord[d]%r.ld[d];
      }
    T_thread[D] = 0;
    x_thread[D] = total_coords.coord[D];
    thread_coords.set_index(x_thread);
    thread.set_index(T_thread);

    //convert to coordinates with ghosts
    r.convertCoordinates(thread_coords_gh, thread_coords); 

    // check if the site is in the current thread
    correct_thread = thread.index == r.thread_id;

  }
  
#pragma omp barrier
  v.setZero();
  v(thread_coords_gh.index,0) = T(correct_thread);
}


template <typename T>
void KPM_Vector <T, 3>::build_planewave(Eigen::Matrix<double,Eigen::Dynamic,1> & k, Eigen::Matrix<T,Eigen::Dynamic,1> & weight){
  
    // Builds an initial vector which is a plane wave with a specific value of k
    // weight is the weight of each orbital for this plane wave 
    // |k> = sum_{r,R} w(R) exp(i k.r + i k.R) |r,R>
    // r = lattice vector
    // R = orbital vector
    // w = weight (only depends on orbital)

    if(weight.rows() != r.Orb)
        std::cout << "Warning in build_planewave: the weight matrix must have the same number"
            " of elements as the number of orbitals.";


    index = 0;    // sets the KPM index to 0
    Coordinates<std::size_t, D + 1> local_coords(r.Ld), global_coords(r.Lt);

    Eigen::Map<Eigen::Matrix<std::size_t, 3, 1>> position(global_coords.coord); // spacial part of the coord vector in global_coords
    auto orb_a_coords = r.rLat.inverse() * r.rOrb;          // column i is the position of the i-th orbital in basis a
                                                            // r.rLat.inverse() each row is a bi / 2*M_PI 
    Eigen::Array<T, Eigen::Dynamic, 1> exp_R;
    exp_R = Eigen::Array<T, Eigen::Dynamic, 1>::Zero(r.Orb, 1);   // exponential related to the orbital
    T exp_r;                                                // exponential related to the lattice site

    // Calculate the exponential related to the orbital exp(i k R) w(R)
    // It is already divided by the norm, which is the number of total sites r.Nt
    for(std::size_t io = 0; io < r.Orb; io++)
        exp_R(io) = weight(io)*exp(assign_value(0, 2.0*M_PI*orb_a_coords.col(io).transpose()*k))/static_cast<T>(sqrt(r.Nt));


    // Calculate the exponential related to each unit cell
    for(std::size_t i2 = NGHOSTS; i2 < r.Ld[2] - NGHOSTS; i2++)
      for(std::size_t i1 = NGHOSTS; i1 < r.Ld[1] - NGHOSTS; i1++)
        for(std::size_t i0 = NGHOSTS; i0 < r.Ld[0] - NGHOSTS; i0++)
          {
            local_coords.set({i0,i1,i2, std::size_t(0)});
            r.convertCoordinates(global_coords, local_coords);          // Converts the coordinates within a thread to global coordinates
            
            exp_r = exp(assign_value(0,  2.0*M_PI * position.cast<double>().transpose()*k ));
            
            for(std::size_t io = 0; io < r.Orb; io++) {
                local_coords.set({i0,i1,i2,io});
                v(local_coords.index, 0) = exp_r*exp_R(io);
              }
          }
    KPM_VectorBasis<T,3u>::build_defect_planewave(k, weight);
}


#define instantiateTYPE(type)               template class KPM_Vector <type,3u>; \
  template void KPM_Vector<type,3u>:: KPM_MOTOR<0u,false>(KPM_Vector<type,3u> * kpm_final, unsigned axis); \
  template void KPM_Vector<type,3u>:: KPM_MOTOR<1u,false>(KPM_Vector<type,3u> * kpm_final, unsigned axis); \
  template void KPM_Vector<type,3u>:: KPM_MOTOR<0u,true>(KPM_Vector<type,3u> * kpm_final, unsigned axis);

instantiateTYPE(float)
instantiateTYPE(double)
instantiateTYPE(long double)
instantiateTYPE(std::complex<float>)
instantiateTYPE(std::complex<double>)
instantiateTYPE(std::complex<long double>)
