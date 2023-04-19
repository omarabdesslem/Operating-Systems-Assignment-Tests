#include <openssl/evp.h>

int digest_message(char* msg, const EVP_MD *md) ;
int digest_fichier(char* nom_du_fichier,const EVP_MD *md);
