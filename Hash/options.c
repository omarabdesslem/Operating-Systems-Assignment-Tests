#include <ctype.h> //pour les fct de char/char*
#include <stdio.h>
#include <stdlib.h> //gestion de memoire, malloc, free
#include <unistd.h>
#include "options.h"
#include <string.h>

int options(int argc, char **argv, const EVP_MD **md_ptr, int *fileoption, int *t_exists, int *t_value_exists)
{
  char *tvalue;
  int index;
  int c;
  *fileoption = 0;
  *t_exists = 0;
  *t_value_exists = 0;

  while ((c = getopt (argc, argv, "ft:")) != -1) {
    switch (c)
      {
      case 'f':
        *fileoption = 1;
        break;
      case 't':
	tvalue = optarg;
	if (tvalue != NULL) {
	  *t_value_exists = 1;
	  *t_exists = 1;
	  if (strcmp(optarg, "md5") == 0) {
	    *md_ptr = EVP_get_digestbyname(tvalue);
	  }
	  else fprintf (stderr, "%s not a valid digest type.\n", optarg);
	}
        break;
      case '?':
        if (optopt == 't')
          fprintf (stderr, "Option -%c requires an argument.\n", optopt);
        else if (isprint (optopt)){
          fprintf (stderr, "Unknown option `-%c'.\n", optopt);}
         else if (optopt == '\0') {
  	  return 0;
				}
        else
          fprintf (stderr, "Unknown option character `\\x%x'.\n\n", optopt);
      default:
        abort ();
      }
    }

  return 1;
}

/*int main(int argc, char **argv){
const EVP_MD *md;
int fileoption = 0;
int t_exists = 0;
printf("%d", options(argc, argv, md, &fileoption, &t_exists));
return 0;
}*/
