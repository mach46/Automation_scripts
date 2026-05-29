#!/bin/bash
#SBATCH --job-name=rotation_d2_5k_rpm_2nd_order
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=12:00:00
#SBATCH --output=/scratch/24cr60r06/dhairya/data_files/out_files/rotation_d2_5k_rpm_2nd_order.out
#SBATCH --error=/scratch/24cr60r06/dhairya/data_files/out_files/rotation_d2_5k_rpm_2nd_order.err
#SBATCH --mail-type=ALL             
#SBATCH --mail-user=pateldn04@gmail.com    

module --force purge
module load apps/ansys/2023r2/AllModules

cd $SLURM_SUBMIT_DIR


# === HOSTFILE SETUP ===
srun hostname -s | sort > hosts.$SLURM_JOB_ID

echo $SLURM_NTASKS > kxfluent.out
cat hosts.$SLURM_JOB_ID >> kxfluent.out

# === FLUENT EXECUTABLE ===
EXE=/home/apps/ANSYS2023R2/installdir/v232/fluent/bin/fluent

# === RUN FLUENT ===
$EXE 3ddp -t$SLURM_NTASKS -pdefault -mpi=default -ssh -cnf=hosts.$SLURM_JOB_ID -g -i /scratch/24cr60r06/dhairya/data_files/temp_jou/temp_rotation_d2_5k_rpm_2nd_order.jou > /scratch/24cr60r06/dhairya/data_files/temp_log/fluent_export_rotation_d2_5k_rpm_2nd_order.log

