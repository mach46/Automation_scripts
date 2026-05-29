#!/bin/bash
#SBATCH --job-name=cfdpost_rotation_d2_5k_rpm_2nd_order
#SBATCH --output=/scratch/24cr60r06/dhairya/data_files/cfdpost_out_files/cfdpost_rotation_d2_5k_rpm_2nd_order.out
#SBATCH --error=/scratch/24cr60r06/dhairya/data_files/cfdpost_out_files/cfdpost_rotation_d2_5k_rpm_2nd_order.err
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --time=02:00:00
#SBATCH --mail-type=ALL             
#SBATCH --mail-user=pateldn04@gmail.com    

cd $SLURM_SUBMIT_DIR


module --force purge
module load apps/python-package/python/conda-python/3.7_new
module load apps/ansys/2023r2/AllModules


python3 "/scratch/24cr60r06/dhairya/data_files/python_files/full_script_bash.py" "d2" "5k"
python3 "/scratch/24cr60r06/dhairya/data_files/python_files/state_point_extraction_bash.py" "d2" "5k"

cfdpost -batch "/scratch/24cr60r06/dhairya/data_files/session_files/state_point_files/rotation_d2_5k_state_point.cse" -results "/scratch/24cr60r06/dhairya/data_files/full_data/rotation_d2_5k_rpm_2nd_order_fulldata.dat" > "/scratch/24cr60r06/dhairya/data_files/cfdpost_data_logs/cfdpost_rotation_d2_5k_rpm_2nd_order_state.log" 2>&1

cfdpost -batch "/scratch/24cr60r06/dhairya/data_files/session_files/flow_path_files/d2_5k_script.cse" -results "/scratch/24cr60r06/dhairya/data_files/full_data/rotation_d2_5k_rpm_2nd_order_fulldata.dat" > "/scratch/24cr60r06/dhairya/data_files/cfdpost_data_logs/cfdpost_rotation_d2_5k_rpm_2nd_order_flow.log" 2>&1

