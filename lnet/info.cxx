#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define MAXBUFLEN 8192
int rank, nprocs;
int subsize, subrank, nidname;
char pname[64];

char * getinfo(char *fname) {

  char *buf;
  buf = (char *) malloc( 1024 * sizeof(char));

  FILE *fp = fopen(fname,"r");
  if (fp == NULL)
    return NULL;

  fgets(buf, MAXBUFLEN, fp);
  fclose(fp);
  return buf;

}

void getLNETroute() {

   char *buf = new char[MAXBUFLEN];
   char *routesconf = new char[MAXBUFLEN];
   char *ip2nets = new char[MAXBUFLEN];
   char *routes = new char[MAXBUFLEN];
   char *stats = new char[MAXBUFLEN];

   routesconf = getinfo ("/etc/lnet/routes.conf");
   ip2nets = getinfo ("/etc/lnet/ip2nets.conf");
   routes = getinfo ("/proc/sys/lnet/routes");
   stats = getinfo ("/proc/sys/lnet/stats");

   //system ("grep current_conn /proc/fs/lustre/osc/snx11214-OST00*/import");
   //buf = getinfo ("/proc/fs/lustre/osc/snx11214-OST00*/ost_conn_uuid"); 

   if (subrank == 0) {
      puts(routesconf);
      //puts(stats);
      system ("cat /etc/lnet/routes.conf");
   }  
}

int main(int argc, char* argv[]) {

   int resultlen; 
   MPI_Comm subcomm;
   
   MPI_Init (&argc, &argv);
   MPI_Comm comm = MPI_COMM_WORLD;
   MPI_Comm_size(comm, &nprocs);
   MPI_Comm_rank(comm, &rank);

   MPI_Get_processor_name(pname, &resultlen);
   nidname = atoi(&pname[3]);

   MPI_Comm_split(comm, nidname, rank, &subcomm); 
   MPI_Comm_size(subcomm, &subsize);
   MPI_Comm_rank(subcomm, &subrank);
   printf("pname of %d %s : nidname %d: %d of %d\n", rank, pname, nidname, subrank, subsize);
  
   getLNETroute();  
   MPI_Finalize();

   return 0;
}

