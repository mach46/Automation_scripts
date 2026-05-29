# Automation Scripts for CFD Workflow

## Overview

This repository contains a collection of shell scripts and utilities developed to automate the CFD workflow from case preparation to post-processing. The objective is to reduce manual effort, ensure consistent case management, and streamline the execution of large parametric studies on HPC systems.

The workflow automates:

* Case preparation
* File organization
* HPC uploads
* CFD execution support
* Result export
* Post-processing and data extraction

---

## Workflow

The overall workflow implemented by these scripts is shown below:

```text
Geometry Creation
        │
        ▼
Mesh Generation
(4 different geometries/cases)
        │
        ▼
Case Generation
(4 Fluent case files)
        │
        ▼
case_rename.sh
(creates multiple copies of files from the previous cases - create only the ones which can be edited through a journal file)
        │
        ▼
batch_upload.sh
(Upload cases to HPC)
        │
        ▼
CFD Simulation on HPC
        │
        ▼
fluent_export.sh
(Convert CFF files to legacy format
and calculate derived variables)
        │
        ▼
cfd_post_processing.sh
(Extract and organize results)
        │
        ▼
Performance Analysis
```

---

## Workflow Description

### 1. Geometry Creation

The CFD workflow begins with the creation of the computational geometry. Multiple geometric configurations can be generated depending on the design parameters under investigation.

### 2. Mesh Generation

Each geometry is discretized into a computational mesh suitable for CFD analysis.

In the present study, four different configurations are meshed, resulting in four independent CFD models.

### 3. Case Generation

The mesh files are imported into ANSYS Fluent, where:

* Material properties are assigned
* Boundary conditions are specified
* Solver settings are configured
* Initialization procedures are defined

This process produces the Fluent case files required for simulation.

### 4. Case Renaming

The generated cases are standardized using automated naming, and copying the case files to create multiple files for parameter study(the ones which can be edited through a .jou file).

### 5. HPC Upload

All simulation files are transferred to the HPC cluster for execution.

### 6. CFD Simulation

The uploaded cases are executed using ANSYS Fluent in batch mode on HPC resources.

### 7. Fluent Export

After simulation completion, Fluent result files in CFF format (`.cas.h5` & `.dat.h5`) are processed and exported in legacy format with additional variable quantities (`.cas` & `.dat`).

### 8. Post-Processing

The exported data is automatically processed to extract key performance metrics and organize the results for further analysis and visualization.

---

## Repository Structure

### `case_rename.sh`

Automatically copies and renames generated CFD cases according to the parametric study.

---

### `batch_upload.sh`

Creates the supporting fluent journal (`.jou`) and HPC cluster job submission (`.sh`) and submits each job.
* sample journal file - `rotation_d2_5k_rpm.jou`
* sample shell file - `rotation_d2_5k_rpm.sh`

---

### `fluent_export.sh`

Submits individual jobs for extracting more data and saving them as `.cas` & `.dat`.
* sample journal file - `temp_rotation_d2_5k_rpm.jou`
* sample shell file - `temp_rotation_d2_5k_rpm.sh`

---

### `cfd_post_processing.sh`

Submits individual jobs and does the following task 
* creates the session files (`.cse`) by running the python script(`full_script_bash.py` & `state_point_extraction_bash.py`) for particular data point.
* opens CFD Post and runs the said cse files.
* CFD post saves the data in `.csv` format at the location specified in the session file.

---

### `data_analysis_bash.py`
opens the exported data files and analysis them and generates required graphs.
