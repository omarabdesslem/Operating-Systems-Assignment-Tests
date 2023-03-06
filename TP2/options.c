#include <ctype.h> //pour les fct de char/char*
#include <stdio.h>
#include <stdlib.h> //gestion de memoire, malloc, free
#include <unistd.h>
#include "options.h"


int options(int argc, char **argv, const EVP_MD *md,  int *fileoption,int* t_exists)
{
  char *tvalue;
  int index;
  int c;
  fileoption, t_exists, opterr = 0, 0, 0 ;

  while ((c = getopt (argc, argv, "ft:")) != -1) {
    switch (c)
      {
      case 'f':
        *fileoption = 1;
        printf("f exists   \n \n");
        printf("  \n");
        break;
      case 't':
        tvalue = optarg;
        *t_exists = 1;
	md = EVP_get_digestbyname(tvalue);
	printf("t exists\n");
  printf("  \n");
        break;
      case '?':
        if (optopt == 't')
          fprintf (stderr, "Option -%c requires an argument.\n", optopt);  
        else if (isprint (optopt))
          fprintf (stderr, "Unknown option `-%c'.\n", optopt);
        else
          fprintf (stderr, "Unknown option character `\\x%x'.\n\n", optopt);
      default:
        abort ();
      }
              }  
       if (md == 0) md = EVP_get_digestbyname("sha1"); 
}

/*int main(int argc, char **argv){
const EVP_MD *md;
int fileoption = 0;
int t_exists = 0;
printf("%d", options(argc, argv, md, &fileoption, &t_exists));
return 0;
}*/
