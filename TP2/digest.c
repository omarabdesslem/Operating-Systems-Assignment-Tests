#include <stdio.h>
#include <string.h>
#include "digest.h"
#include <openssl/evp.h>
#include <stdlib.h> //gestion de memoire, malloc, free
#include <unistd.h>



int digest_message(char* msg, const EVP_MD *md)
///prend comme paramètres le msg qu'on va hashé
{
    EVP_MD_CTX *mdctx;
    unsigned char md_value[EVP_MAX_MD_SIZE];
    unsigned int md_len;
    int i;
    md = EVP_get_digestbyname("sha1");
    mdctx = EVP_MD_CTX_new(); //create structure of EVP_MD_CTX
    EVP_DigestInit_ex(mdctx, md, NULL);
    EVP_DigestUpdate(mdctx, msg, strlen(msg)); //processes the input string
    EVP_DigestFinal_ex(mdctx, md_value, &md_len); //calculates the final hash value
    for (i = 0; i < md_len-1; i++)
        printf("%02x", md_value[i]);
    printf("  %s\n",msg);
    EVP_MD_CTX_free(mdctx);

    return 0;
}


int digest_fichier(char* nom_du_fichier, const EVP_MD *md) //prend comme paramètres le message_digest_type (sha1, sha256), le msg qu'on va hashé
{
    EVP_MD_CTX *mdctx;
    unsigned char md_value[EVP_MAX_MD_SIZE];
    unsigned int md_len, i;
    unsigned char buf[4096];
    md = EVP_get_digestbyname("sha1");
    size_t n;
    printf("Initialisation OK\n");
    FILE *f = fopen(nom_du_fichier, "r");
    if (f == NULL) {
        printf("Ce fichier n'existe pas\n");
       return 0;
    }


    mdctx = EVP_MD_CTX_new(); //create structure of EVP_MD_CTX
    EVP_DigestInit_ex(mdctx, md, NULL);
    while ((n = fread(buf, 1, sizeof(buf), f)) > 0) {
    EVP_DigestUpdate(mdctx, nom_du_fichier, strlen(nom_du_fichier)); //processes the input string
    }
    EVP_DigestFinal_ex(mdctx, md_value, &md_len); //calculates the final hash value
    

    for (i = 0; i < md_len; i++)
        printf("%02x", md_value[i]);
    printf("  %s\n",nom_du_fichier);
    EVP_MD_CTX_free(mdctx);

    return 0;
}



/*int main(){
char* msg="le man disait";
printf("%d", digest_message(msg));
digest_fichier("texte.txt");
return 0;}*/

