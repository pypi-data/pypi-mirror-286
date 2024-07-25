/***********************************************************/
/*                                                         */
/*   Copyright (C) 2018-2022, M. Andelkovic, L. Covaci,    */
/*  A. Ferreira, S. M. Joao, J. V. Lopes, T. G. Rappoport  */
/*                                                         */
/***********************************************************/

#define outcol "\033[1;31m"
#define outres "\033[0m"

#ifndef DEBUG
#define DEBUG 0
#endif

#ifndef VERBOSE
#define VERBOSE 1
#endif

// The first scale is 1/2pi and corresponds to the conductance quantum per spin e^2/h
// The second scale is the universal conductivity of graphene e^2/4h_bar
#define scale1 0.159154943
#define scale2 0.25
#define unit_scale 0.159154943

#ifndef VERBOSE_MESSAGES
    #define VERBOSE_MESSAGES 1
    #ifdef VERBOSE
        #if VERBOSE==1
                #define verbose_message(VAR) std::cout<<VAR<<std::flush
        #else
            #define verbose_message(VAR)
        #endif
    #else
        #define verbose_message(VAR)
    #endif
#endif

#ifdef DEBUG
	#if DEBUG==1
		#define debug_message(VAR) std::cout << outcol << VAR << outres << std::flush
		#define verbose_message(VAR) std::cout<<VAR<<std::flush
	#else
		#define debug_message(VAR) 
	#endif
#else
	#define debug_message(VAR) 
#endif

#ifndef M_PI
#define M_PI   3.14159265358979323846264338327950288
#endif
