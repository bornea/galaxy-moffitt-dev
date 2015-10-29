#ifndef ATL_sGetNB_geqrf

/*
 * NB selection for GEQRF: Side='RIGHT', Uplo='UPPER'
 * M : 25,216,504,1008,1512,2016,4104
 * N : 25,216,504,1008,1512,2016,4104
 * NB : 9,72,72,72,72,144,216
 */
#define ATL_sGetNB_geqrf(n_, nb_) \
{ \
   if ((n_) < 120) (nb_) = 9; \
   else if ((n_) < 1764) (nb_) = 72; \
   else if ((n_) < 3060) (nb_) = 144; \
   else (nb_) = 216; \
}


#endif    /* end ifndef ATL_sGetNB_geqrf */
