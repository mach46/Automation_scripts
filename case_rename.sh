#!/bin/bash
#SBATCH --job-name=case_rename
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=01:00:00
#SBATCH --output=case_rename.out
#SBATCH --error=case_rename.err
#SBATCH --mail-type=BEGIN,FAIL,END               
#SBATCH --mail-user=pateldn04@gmail.com    


# === RANGES ===
D_RANGE=("d2" "d3" "d4" "d5")
RPM_RANGE=("30k" "35k" "40k" "45k" "50k" "55k" "60k" "65k" "70k")

# === DIRECTORIES ===
BASE_DIR=$(pwd)
CASE_DIR="$BASE_DIR/case_files"

# === CREATE COPIES ===
for d in "${D_RANGE[@]}"; do

    source_case="$CASE_DIR/rotation_${d}_5k_rpm.cas.h5"

    # Check source exists
    if [ ! -f "$source_case" ]; then
        echo "Missing source file: $source_case"
        continue
    fi

    for rpm in "${RPM_RANGE[@]}"; do

        target_case="$CASE_DIR/rotation_${d}_${rpm}_rpm.cas.h5"

        cp "$source_case" "$target_case"

        echo "Created: $target_case"

    done

done