#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <mpi.h>

#include "xctopo.h"

int main(int argc, char * argv[])
{
  int rc;
  int rank, size;

  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  int nid;
  FILE *nidfile = fopen("/proc/cray_xt/nid", "r");
  if (nidfile!=NULL) 
    fscanf(nidfile, "%d", &nid);
  fclose(nidfile);

  xctopo_t topo;
  rc = xctopo_get_mycoords(&topo);

  int col   = topo.col;
  int row   = topo.row;
  int cage  = topo.cage;
  int slot  = topo.slot;
  int anode = topo.anode;

  printf("%d %d %d %d %d %d %d \n", rank, nid, col, row, cage, slot, anode);

  MPI_Finalize();

  return 0;
}
