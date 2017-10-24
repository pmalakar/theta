#!/bin/bash -l
#COBALT -A Performance
#COBALT -n 4

#SBATCH -p debug
#SBATCH -t 00:10:00
#SBATCH -N 2
#SBATCH -J my_job
#SBATCH -C knl,quad,cache    ####haswell
##SBATCH -o my_job.o%j


export MPICH_MPIIO_HINTS_DISPLAY=1
export MPICH_MPIIO_AGGREGATOR_PLACEMENT_DISPLAY=1 
export MPICH_MPIIO_STATS=1
export MPICH_MPIIO_XSTATS=1
export MPICH_MPIIO_TIMERS=1

echo "***"

EXE="./info"

if [[ "$HOST" == *"cori"* ]]; then
#cori
echo "cori"
grep current_conn /proc/fs/lustre/osc/snx11168-OST00*/import
cat /proc/fs/lustre/osc/snx11168-OST00*/ost_conn_uuid 
nodes=$SLURM_JOB_NUM_NODES
echo $SLURM_NODELIST
srun -n 4 -N 2 ${EXE} #./status.knl
fi

if [[ "$HOST" == *"theta"* ]]; then
#theta

echo "theta"
ppn=2
RANKS=$((${COBALT_PARTSIZE}*$ppn))

APRUNPARAMS=" -n ${RANKS} -N ${ppn} -d 1 -j 1 -r 1 " #--attrs mcdram=cache:numa=quad "
ENVVARS=""

#grep current_conn /proc/fs/lustre/osc/snx11214-OST00*/import
#cat /proc/fs/lustre/osc/snx11214-OST00*/ost_conn_uuid 
#cat /proc/sys/lnet/routes
#cat /proc/sys/lnet/stats

aprun ${ENVVARS} ${APRUNPARAMS} ${EXE}

fi

echo "***"
