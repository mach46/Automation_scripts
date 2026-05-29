#!/bin/bash


#SBATCH --job-name=rotation_d2_5k_rpm
#SBATCH -p medium
#SBATCH --nodes=3
#SBATCH --ntasks-per-node=40
#SBATCH --mail-type=BEGIN,FAIL,END               # Send email at job completion
#SBATCH --mail-user=pateldn04@gmail.com    # Email address for notifications
#SBATCH --time=12:00:00


module --force purge
module load apps/ansys/2023r2/AllModules
srun hostname -s | sort > hosts.$SLURM_JOB_ID

echo $SLURM_NTASKS > kxfluent.out
cat hosts,$SLURM_JOB_ID >> kxfluent.out
EXE=/home/apps/ANSYS2023R2/installdir/v232/fluent/bin/fluent
# Run FLUENT
$EXE 3ddp -t$SLURM_NTASKS -pdefault -mpi=default -ssh -cnf=hosts.$SLURM_JOB_ID -g -i rotation_d2_5k_rpm.jou > rotation_d2_5k_rpm.out
