/***********************************************************/
/*                                                         */
/*   Copyright (C) 2018-2022, M. Andelkovic, L. Covaci,    */
/*  A. Ferreira, S. M. Joao, J. V. Lopes, T. G. Rappoport  */
/*                                                         */
/***********************************************************/


#include "Generic.hpp"
#include "tools/ComplexTraits.hpp"
#include "tools/Random.hpp"
#include <cmath>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
template <typename T>
KPMRandom<T>::KPMRandom() {
  init_random();
}

template <typename T>
void KPMRandom<T>::init_random()
{
    // only for MSVC
    #ifdef _MSC_VER
    size_t requiredSize = 0;
    getenv_s(&requiredSize, nullptr, 0, "SEED");
    if (requiredSize == 0) {
        // SEED not found, use random_device as before
        std::random_device r;
        std::array<int, 624> seed_data;
        std::generate(seed_data.begin(), seed_data.end(), std::ref(r));
        std::seed_seq seq(std::begin(seed_data), std::end(seed_data));
        rng.seed(seq);
    } else {
        // SEED found, use it
        std::vector<char> seedValue(requiredSize);
        getenv_s(&requiredSize, seedValue.data(), requiredSize, "SEED");
        rng.seed(atoi(seedValue.data()));
    }
    #else
    char *env;
    env = getenv("SEED");
    if(env==NULL){
        // Didn't find the seed
        std::random_device r;
        std::array<int, 624> seed_data;
        std::generate(seed_data.begin(), seed_data.end(), std::ref(r));
        std::seed_seq seq(std::begin(seed_data), std::end(seed_data));
        rng.seed(seq);
    }
    else {
        // Found the seed
        rng.seed(atoi(env));
    }
    #endif
}

template <typename T>
double  KPMRandom<T>::get() {
  return dist(rng);
}
template <typename T>
double KPMRandom<T>::uniform(double  mean, double  width) {
    // mean  : mean value
    // width : root mean square deviation
  return mean + sqrt(3.) * width * (2 * dist(rng)  - 1);
}
template <typename T>
double KPMRandom<T>::gaussian(double  mean, double  width) {
  // mean  : mean value
  // width : root mean square deviation
  return mean + width*gauss(rng);
}

template <typename T>
template <typename U>
typename std::enable_if<is_tt<std::complex, U>::value, U>::type KPMRandom<T>::initA() {
  return exp(T(0., value_type(2*M_PI*dist(rng)) ));
}

template <typename T>
template <typename U>
typename std::enable_if<!is_tt<std::complex, U>::value, U>::type KPMRandom<T>::initA() {
    return (2*dist(rng) - 1.)*sqrt(3);
}

template <typename T>
T KPMRandom<T>::init(){
  return initA<T>();
}
  
template class KPMRandom<float>;
template class KPMRandom<double>;
template class KPMRandom<long double>;

template class KPMRandom<std::complex<float>>;
template class KPMRandom<std::complex<double>>;
template class KPMRandom<std::complex<long double>>;
