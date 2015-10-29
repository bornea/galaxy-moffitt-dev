#ifndef ATLAS_TRSMNB_H
   #define ATLAS_TRSMNB_H

   #ifdef SREAL
      #define TRSM_NB 216
   #elif defined(DREAL)
      #define TRSM_NB 112
   #elif defined(SCPLX)
      #define TRSM_NB 80
   #elif defined(DCPLX)
      #define TRSM_NB 56
   #endif

#endif
