#!/bin/bash -l
#COBALT -t 30
####COBALT -n 1
#COBALT -A CSC250STDM10 ##Performance

#SBATCH -p debug
#SBATCH -t 00:10:00
#SBATCH -N 2
#SBATCH -J my_job
#SBATCH -C knl,quad,cache    ####haswell
##SBATCH -o my_job.o%j


EXE=./location.x

echo "***"

if [[ "$HOST" == *"cori"* ]]; then
#cori
echo "cori"
grep current_conn /proc/fs/lustre/osc/snx11168-OST00*/import
cat /proc/fs/lustre/osc/snx11168-OST00*/ost_conn_uuid 
nodes=$SLURM_JOB_NUM_NODES
echo $SLURM_NODELIST
srun -n 4 -N 2 ${EXE}
fi

if [[ "$HOST" == *"theta"* ]]; then
#theta
echo "theta"
ppn=4
RANKS=$((${COBALT_PARTSIZE}*$ppn))

APRUNPARAMS=" -n ${RANKS} -N ${ppn} -d 1 -j 1 -r 1 " #--attrs mcdram=cache:numa=quad "
ENVVARS=""

grep current_conn /proc/fs/lustre/osc/snx11214-OST00*/import
cat /proc/fs/lustre/osc/snx11214-OST00*/ost_conn_uuid 

aprun ${ENVVARS} ${APRUNPARAMS} ${EXE}

fi
echo "***"
