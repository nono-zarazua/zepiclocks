#!/bin/bash

cd "$(dirname "$0")"

echo "Downloading clock coefficients..."
wget -O hovarth_sites.csv https://static-content.springer.com/esm/art%3A10.1186%2Fgb-2013-14-10-r115/MediaObjects/13059_2013_3156_MOESM3_ESM.csv

wget -O phenoage_cpgs.csv https://cdn.aging-us.com/article/101414/supplementary/SD2/0/aging-v10i4-101414-supplementary-material-SD2.csv 

wget -O physage_cpgs.txt https://raw.githubusercontent.com/em-arpy/DNAm_PhysAge/main/CpG%20lists%20and%20weights/HRS_cpg_training_means.txt

echo "Fetching RAW Zhou Lab support files (GRCh38)..."
wget -O EPICv2.hg38.manifest.tsv.gz https://raw.githubusercontent.com/zhou-lab/InfiniumAnnotationV1/main/Anno/EPICv2/EPICv2.hg38.manifest.tsv.gz

wget -O EPICv2.hg38.manifest.gencode.v41.tsv.gz https://raw.githubusercontent.com/zhou-lab/InfiniumAnnotationV1/main/Anno/EPICv2/EPICv2.hg38.manifest.gencode.v41.tsv.gz

wget -O EPICv2.hg38.mask.tsv.gz https://raw.githubusercontent.com/zhou-lab/InfiniumAnnotationV1/main/Anno/EPICv2/EPICv2.hg38.mask.tsv.gz

echo "Running DunedinPACE extraction..."
./download_dunedinpace.py

echo "Running coordinate matching and biological QC pipeline..."
./clean_csvs.py
