#!/bin/bash
#SBATCH --job-name=batch_upload
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=01:00:00
#SBATCH --output=batch_upload.out
#SBATCH --error=batch_upload.err
#SBATCH --mail-type=ALL            
#SBATCH --mail-user=pateldn04@gmail.com    

# === RANGES ===
D_RANGE=("d3" "d4" "d5")
RPM_RANGE=("30k" "35k" "40k" "45k" "50k" "55k" "60k" "65k" "70k")

# === DIRECTORIES ===
BASE_DIR=$(pwd)

CASE_DIR="$BASE_DIR/case_files"
JOU_DIR="$BASE_DIR/journal_files"
SH_DIR="$BASE_DIR/shell_files"
DATA_DIR="$BASE_DIR/data_files"


# === MASS FLOW RATES ===
declare -A MASSFLOW

MASSFLOW["d2"]=0.04
MASSFLOW["d3"]=0.09
MASSFLOW["d4"]=0.16
MASSFLOW["d5"]=0.25


# === LOOP ===
for d in "${D_RANGE[@]}"; do
  for rpm in "${RPM_RANGE[@]}"; do

    base="rotation_${d}_${rpm}_rpm"
    casfile="$CASE_DIR/${base}.cas.h5"

    # Check if case exists
    if [ ! -f "$casfile" ]; then
      echo "Skipping $casfile (not found)"
      continue
    fi

    echo "Processing $base"

    # =========================
    # JOURNAL FILE
    # =========================
    joufile="$JOU_DIR/${base}.jou"
    
    # Extract numeric RPM value (e.g. 50k -> 50000)
    rpm_value=$(echo "$rpm" | sed 's/k/000/')
    # Extract numeric diameter value (e.g. d2 -> 0.002)
    diameter_m=$(echo "$d" | sed 's/d/0.00/')
    
    massflow=${MASSFLOW[$d]}

    # Convert RPM to rad/s
    omega=$(awk "BEGIN {printf \"%.6f\", $rpm_value * 2 * 3.141592653589793 / 60}")

    cat << EOF > "$joufile"
/file/read-case ${casfile}

; Boundary conditions  Relative frame of reference
/define/boundary-conditions/mass-flow-inlet inlet no yes yes no ${massflow} no 266.5307069999999 no 9000000 no yes no no no yes 5 ${diameter_m}
/define/boundary-conditions/pressure-outlet outlet no yes no 6244708.979564001 no 263.698489 no yes no no no yes 5 ${diameter_m} no yes no no no
/define/boundary-conditions/fluid/ fluid no no no yes -1 no ${omega} no 0 no 0 no 0 no 0 no 0 no 0 no 0 no 0 no 1 none no no -1 no no no


/solve/monitors/residual/convergence-criteria 1e-6 1e-6 1e-6 1e-6 1e-6 1e-6 1e-6

/solve/initialize/hyb-initialization 


; First-order phase
/solve/set/discretization-scheme density 0
/solve/set/discretization-scheme mom 0
/solve/set/discretization-scheme k 0
/solve/set/discretization-scheme omega 0
/solve/set/discretization-scheme temperature 0

/solve/iterate 2000

; Switch to second-order
/solve/set/discretization-scheme density 1
/solve/set/discretization-scheme mom 1
/solve/set/discretization-scheme k 1
/solve/set/discretization-scheme omega 1
/solve/set/discretization-scheme temperature 1

/solve/iterate 3000

/file/write-case-data ${DATA_DIR}/${base}.dat

exit
EOF

    # =========================
    # SHELL FILE
    # =========================
    shfile="$SH_DIR/${base}.sh"

    cat << EOF > "$shfile"
#!/bin/bash
#SBATCH --job-name=${base}
#SBATCH --partition=medium
#SBATCH --nodes=3
#SBATCH --ntasks-per-node=40
#SBATCH --time=12:00:00
#SBATCH --output=${base}.out
#SBATCH --error=${base}.err
#SBATCH --mail-type=ALL             
#SBATCH --mail-user=pateldn04@gmail.com    

module --force purge
module load apps/ansys/2023r2/AllModules

cd \$SLURM_SUBMIT_DIR


# === HOSTFILE SETUP ===
srun hostname -s | sort > hosts.\$SLURM_JOB_ID

echo \$SLURM_NTASKS > kxfluent.out
cat hosts.\$SLURM_JOB_ID >> kxfluent.out

# === FLUENT EXECUTABLE ===
EXE=/home/apps/ANSYS2023R2/installdir/v232/fluent/bin/fluent

# === RUN FLUENT ===
\$EXE 3ddp -t\$SLURM_NTASKS -pdefault -mpi=default -ssh \
-cnf=hosts.\$SLURM_JOB_ID \
-g -i ${joufile} > fluent_${base}.log


EOF

    dos2unix "$shfile"

    # =========================
    # SUBMIT JOB
    # =========================
    sbatch "$shfile"

  done
done