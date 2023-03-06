#include <stdio.h>
#include <stdlib.h> //gestion de memoire, malloc, free
#include <unistd.h>
#include "options.h"
#include "digest.h"
//==>car c'est en dossier courant, on le met avec ""

int main(int argc,char** argv){
  const EVP_MD *md_a;
  md_a = EVP_get_digestbyname("sha1");
  int f=0;
  int fileoption=0;
  int t_exists=0;
  int i = argc - 1;
  options(argc, argv, md_a, &fileoption, &t_exists);
  if (fileoption){
       digest_fichier(argv[i],  md_a);}
  
  else {
    digest_message(argv[i], md_a);}
  
};
