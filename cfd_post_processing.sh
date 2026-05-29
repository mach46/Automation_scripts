#!/bin/bash
#SBATCH --job-name=cfd_post_processing
#SBATCH --output=cfd_post_processing.out
#SBATCH --error=cfd_post_processing.err
#SBATCH --partition=shared  
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=01:00:00
#SBATCH --mail-type=All                      # Send email at job completion
#SBATCH --mail-user=pateldn04@gmail.com      # Email address for notifications

# === DIRECTORIES ===
BASE_DIR=$(pwd)

DATA_DIR="$BASE_DIR/full_data"
SH_DIR="$BASE_DIR/cfdpost_shell_files"
LOG_DIR="$BASE_DIR/cfdpost_data_logs"
OUT_DIR="$BASE_DIR/cfdpost_out_files"

FLOW_PATH_SCRIPT="/scratch/24cr60r06/dhairya/data_files/python_files/full_script_bash.py"
STATE_POINT_SCRIPT="/scratch/24cr60r06/dhairya/data_files/python_files/state_point_extraction_bash.py"

# === RANGES ===
D_RANGE=("d2" "d3" "d4" "d5")
RPM_RANGE=("5k" "10k" "15k" "20k" "25k" "30k" "35k" "40k" "45k" "50k" "55k" "60k" "65k" "70k")

# =========================================
# LOOP OVER ALL CASES
# =========================================

for diameter in "${D_RANGE[@]}"
do

    for rpm in "${RPM_RANGE[@]}"
    do
        base="rotation_${diameter}_${rpm}_rpm_2nd_order"
        
        FLOW_CSE="/scratch/24cr60r06/dhairya/data_files/session_files/flow_path_files/${diameter}_${rpm}_script.cse"
        STATE_CSE="/scratch/24cr60r06/dhairya/data_files/session_files/state_point_files/rotation_${diameter}_${rpm}_state_point.cse"
        
        
        if [ ! -f "${DATA_DIR}/${base}_fulldata.dat" ]; then
          echo "Skipping $base (data file not found)"
          continue
        fi

        echo "=================================="
        echo "Running case:"
        echo "Diameter = $diameter"
        echo "RPM      = $rpm"
        echo "=================================="
        
        
        shfile="$SH_DIR/cfdpost_${base}.sh"

        cat << EOF > "$shfile"
#!/bin/bash
#SBATCH --job-name=cfdpost_${base}
#SBATCH --output=${OUT_DIR}/cfdpost_${base}.out
#SBATCH --error=${OUT_DIR}/cfdpost_${base}.err
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --time=02:00:00
#SBATCH --mail-type=ALL             
#SBATCH --mail-user=pateldn04@gmail.com    

cd \$SLURM_SUBMIT_DIR


module --force purge
module load apps/python-package/python/conda-python/3.7_new
module load apps/ansys/2023r2/AllModules


python3 "$FLOW_PATH_SCRIPT" "$diameter" "$rpm"
python3 "$STATE_POINT_SCRIPT" "$diameter" "$rpm"

cfdpost -batch "$STATE_CSE" \
-results "${DATA_DIR}/${base}_fulldata.dat" \
> "${LOG_DIR}/cfdpost_${base}_state.log" 2>&1

cfdpost -batch "$FLOW_CSE" \
-results "${DATA_DIR}/${base}_fulldata.dat" \
> "${LOG_DIR}/cfdpost_${base}_flow.log" 2>&1

EOF

        # =========================
        # SUBMIT JOB
        # =========================
        sbatch "$shfile"

    done

done

echo "=================================="
echo "ALL CASES COMPLETED"
echo "=================================="