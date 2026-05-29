#!/bin/bash
#SBATCH --job-name=fluent_export
#SBATCH --output=fluent_export.out
#SBATCH --error=fluent_export.err
#SBATCH --partition=shared  
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=10:00:00
#SBATCH --mail-type=All                      # Send email at job completion
#SBATCH --mail-user=pateldn04@gmail.com      # Email address for notifications


# === RANGES ===
D_RANGE=("d2" "d3" "d4" "d5")
RPM_RANGE=("5k" "10k" "15k" "20k" "25k" "30k" "35k" "40k" "45k" "50k" "55k" "60k" "65k" "70k")

# === DIRECTORIES ===
BASE_DIR=$(pwd)

JOU_DIR="$BASE_DIR/temp_jou"
SH_DIR="$BASE_DIR/temp_sh"
LOG_DIR="$BASE_DIR/temp_log"
DATA_DIR="$BASE_DIR/full_data"
OUT_DIR="$BASE_DIR/out_files"

module --force purge
module load apps/ansys/2023r2/AllModules

EXE=/home/apps/ANSYS2023R2/installdir/v232/fluent/bin/fluent


echo "Running in: $PWD"
echo "Using Fluent: $EXE"

# === LOOP ===
for d in "${D_RANGE[@]}"; do
  for rpm in "${RPM_RANGE[@]}"; do
    
    base="rotation_${d}_${rpm}_rpm_2nd_order"
    
    # Check if case exists
    if [ ! -f "$base.cas.h5" ]; then
      echo "Skipping $base (not found)"
      continue
    fi
    
    if [ -f "${DATA_DIR}/${base}_fulldata.dat" ]; then
      echo "Skipping $base (already completed)"
      continue
    fi

    echo "Processing $base ..."
    
    # =========================
    # JOURNAL FILE
    # =========================
    joufile="$JOU_DIR/temp_${base}.jou"

    cat << EOF > "$joufile"
/file/read-case-data ${BASE_DIR}/${base}.cas.h5

/file/binary-legacy-files yes
/file/cff-files no
/file/data-file-options 
; note: 2 enter spaces after this line is required for proper functioning of this code. It is a safety mechanism to bypass the "reset the already defined derived quantities [yes]" prompt otherwise the code may not write the full_data file.


mach-number total-pressure total-temperature total-enthalpy total-energy enthalpy entropy density pressure sound-speed specific-heat-cp gas-constant compressibility-factor density-all dynamic-pressure pressure-coefficient absolute-pressure velocity-magnitude x-velocity y-velocity z-velocity axial-velocity radial-velocity tangential-velocity relative-x-velocity relative-y-velocity relative-z-velocity rel-velocity-magnitude relative-velocity-angle rel-total-pressure rel-total-temperature rothalpy dp-dx dp-dy dp-dz dx-velocity-dx dx-velocity-dy dx-velocity-dz dy-velocity-dx dy-velocity-dy dy-velocity-dz dz-velocity-dx dz-velocity-dy dz-velocity-dz strain-rate-mag vorticity-mag x-vorticity y-vorticity z-vorticity helicity q-criterion raw-q-criterion lambda2-criterion turb-kinetic-energy turb-diss-rate turb-intensity turb-reynolds-number-rey viscosity-turb viscosity-eff viscosity-lam viscosity-ratio thermal-conductivity-eff thermal-conductivity-lam prandtl-number-eff prandtl-number-lam wall-shear x-wall-shear y-wall-shear z-wall-shear wall-temperature wall-adjacent-temperature y-plus y-star skin-friction-coef heat-flux heat-transfer-coef heat-transfer-coef-wall heat-transfer-coef-wall-adj heat-transfer-coef-yplus stanton-number nusselt-number cell-reynolds-number cell-volume cell-volume-change cell-wall-distance mass-imbalance x-coordinate y-coordinate z-coordinate axial-coordinate radial-coordinate angular-coordinate abs-angular-coordinate
quit


/file/write-case-data ${DATA_DIR}/${base}_fulldata.dat

/exit yes

EOF

    # =========================
    # SHELL FILE
    # =========================
    shfile="$SH_DIR/$temp_{base}.sh"

    cat << EOF > "$shfile"
#!/bin/bash
#SBATCH --job-name=${base}
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --time=12:00:00
#SBATCH --output=${OUT_DIR}/${base}.out
#SBATCH --error=${OUT_DIR}/${base}.err
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
-g -i $JOU_DIR/temp_${base}.jou > ${LOG_DIR}/fluent_export_${base}.log

EOF

    dos2unix "$shfile"

    # =========================
    # SUBMIT JOB
    # =========================
    sbatch "$shfile"
    
  done
done