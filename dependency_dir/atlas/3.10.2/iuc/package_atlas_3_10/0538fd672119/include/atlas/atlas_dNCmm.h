#ifndef DMM_H
   #define DMM_H

   #define ATL_mmNOMULADD
   #define ATL_mmLAT 5
   #define ATL_mmMU  4
   #define ATL_mmNU  1
   #define ATL_mmKU  56
   #define MB 64
   #define NB 64
   #define KB 64
   #define NBNB 4096
   #define MBNB 4096
   #define MBKB 4096
   #define NBKB 4096
   #define NB2 128
   #define NBNB2 8192

   #define ATL_MulByNB(N_) ((N_) << 6)
   #define ATL_DivByNB(N_) ((N_) >> 6)
   #define ATL_MulByNBNB(N_) ((N_) << 12)

#endif
