#include <stdio.h>
#include <stdlib.h>
#include <fstream>
#include <mpi.h>

#define MAXBUFLEN 65536

using namespace std;

int rank, nprocs;
int subsize, subrank, nidname;
char pname[64];

//void 
char *getinfo(char *fname) { //, char *buf) {

  ifstream inFile;
  inFile.open(fname);
  filebuf *pbuf = inFile.rdbuf();

  std::size_t size = pbuf->pubseekoff (0, inFile.end, inFile.in);
  pbuf->pubseekpos (0, inFile.in);

  char *buf = new char[size];
  pbuf->sgetn (buf, size);

  inFile.close();

  return buf;
}

void getLNETroute() {

   char *ostconn, *routesconf;
   char *ip2nets, *routes, *stats; 

   if (subrank == 0) {
     routesconf = getinfo ("/etc/lnet/routes.conf"); 
     printf ("%d %d routesconf %s\n", rank, nprocs, routesconf);
     ip2nets = getinfo ("/etc/lnet/ip2nets.conf");
     printf ("%d %d ip2netsconf %s\n", rank, nprocs, ip2nets);
     // getinfo ("/proc/fs/lustre/osc/snx11214-OST00*/ost_conn_uuid", ostconn); 
  //  system ("cat /proc/sys/lnet/routes");
  //  system ("cat /proc/sys/lnet/stats");
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
//   printf("pname of %d %s : nidname %d: %d of %d\n", rank, pname, nidname, subrank, subsize);

   getLNETroute();  
   MPI_Finalize();

   return 0;
}

