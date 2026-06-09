# zepiclocks
Repository to build Zengen's epigenetic clocks pipeline

```text
zepiclocks/
├── README.md
├── Makefile
├── requirements.txt
└── BED/
    └── panel_targeted_cpgs.bed  # The final generated BED file
```

# Zepiclocks: Instruction Manual

Zepiclocks is an automated pipeline that extracts, unifies, and runs quality control on CpG sites from Horvath, PhenoAge, and DunedinPACE epigenetic clocks to generate a targeted `.bed` file for downstream sequencing.

## 🛠️ 1. Prepare Conda Environment

Before running the pipeline, make sure the conda is [installed](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). 

To set up the necessary environment and data, run:

```bash
make all
```
