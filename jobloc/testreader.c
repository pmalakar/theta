#include <stdio.h>
#include <stdlib.h>

#define NUMOSTS 56

struct OST2LNET {

  char ostidx[16];
  char ostib[16];
  char lnets[64];

} *ost2lnet;

int main()
{

 ost2lnet = malloc (NUMOSTS * sizeof (struct OST2LNET*));

 FILE *fp;
 fp = fopen("theta_ost2lnet", "r");
 
 int line=0;

 while(!feof(fp))
 {
  fscanf (fp, "%s %s %s", ost2lnet[line].ostidx, ost2lnet[line].ostib, ost2lnet[line].lnets);
  printf ("%s %s %s\n", ost2lnet[line].ostidx, ost2lnet[line].ostib, ost2lnet[line].lnets);
  line++;
 }

 fclose(fp);

 return 0;

}

