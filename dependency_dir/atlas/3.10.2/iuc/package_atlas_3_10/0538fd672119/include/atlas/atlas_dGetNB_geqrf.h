#ifndef ATL_dGetNB_geqrf

/*
 * NB selection for GEQRF: Side='RIGHT', Uplo='UPPER'
 * M : 25,168,280,392,784,1176,1624,3248
 * N : 25,168,280,392,784,1176,1624,3248
 * NB : 9,14,56,56,56,56,112,112
 */
#define ATL_dGetNB_geqrf(n_, nb_) \
{ \
   if ((n_) < 96) (nb_) = 9; \
   else if ((n_) < 224) (nb_) = 14; \
   else if ((n_) < 1400) (nb_) = 56; \
   else (nb_) = 112; \
}


#endif    /* end ifndef ATL_dGetNB_geqrf */
