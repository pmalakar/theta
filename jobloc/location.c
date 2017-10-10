#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <mpi.h>

#include "xctopo.h"

int rank, size, subrank;

int getNodeInfo ()
{

  int rc;
  int nid, subsize;
  MPI_Comm subcomm;
  char pname[64];
  //FILE *nidfile = fopen("/proc/cray_xt/nid", "r");
  //if (nidfile!=NULL) 
  //  fscanf(nidfile, "%d", &nid);
  //fclose(nidfile);

  MPI_Get_processor_name(pname, &rc);
  nid = atoi(&pname[3]);
  MPI_Comm_split(MPI_COMM_WORLD, nid, rank, &subcomm); 
  MPI_Comm_size(subcomm, &subsize);
  MPI_Comm_rank(subcomm, &subrank);
//  printf("pname of %d %s : nidname %d: %d of %d\n", rank, pname, nidname, subrank, subsize);
  
  xctopo_t topo;
  rc = xctopo_get_mycoords(&topo);

  int col   = topo.col;
  int row   = topo.row;
  int cage  = topo.cage;
  int slot  = topo.slot;
  int anode = topo.anode;

  printf("%d (%d) %d %d %d %d %d %d\n", rank, subrank, nid, col, row, cage, slot, anode);

  return 0;

}

int main(int argc, char * argv[])
{
  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  getNodeInfo();

  MPI_Finalize();

  return 0;
}
