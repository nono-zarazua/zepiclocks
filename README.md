# zepiclocks
Repository to build Zengen's epigenetic clocks pipeline

# Zepiclocks: Instruction Manual

Zepiclocks is an automated pipeline that extracts, unifies, and runs quality control on CpG sites from Horvath, PhenoAge, and DunedinPACE epigenetic clocks to generate a targeted `.bed` file for downstream sequencing.

## 🛠️ 1. Install Python Packages

Before running the pipeline, you must install the required Python packages. Run the following command in your terminal:

```bash
pip install pandas pyaging
```

To set up the necessary data run:

```bash
make
```
