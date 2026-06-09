#!/usr/bin/env python3

import pandas as pd
import os
import sys

zhou_gencode = 'EPICv2.hg38.manifest.gencode.v41.tsv.gz'
zhou_manifest = 'EPICv2.hg38.manifest.tsv.gz'
zhou_mask = 'EPICv2.hg38.mask.tsv.gz'
OUTPUT_BED = 'panel_targeted_cpgs.bed'

valid_chroms = [str(i) for i in range(1,23)] + ['X','Y','M']
anchor_genes = ['ELOVL2','FHL2','PENK']

# 1. Parse Horvath 2013
# We use skiprows=2 to ignore the two lines of text/blanks at the top
df_horvath = pd.read_csv('hovarth_sites.csv', skiprows=2)
# Remove duplicates in CPGmarker col and NAs
horvath_cpgs = set(df_horvath['CpGmarker'].dropna())

# 2. Parse PhenoAge
df_pheno = pd.read_csv('phenoage_cpgs.csv')
pheno_cpgs = set(df_pheno['CpG'].dropna())

# 3. Parse DunedinPACE
df_dunedin = pd.read_csv('dunedinpace_173_weights.csv')
dunedin_cpgs = set(df_dunedin['CpG'].dropna())

# 4. Parse PhysAge
df_physage = pd.read_csv('physage_cpgs.txt',sep=' ')
physage_cpgs = set(df_physage['cpg'].dropna())

# 5. Unify the sets
all_cpgs = horvath_cpgs.union(pheno_cpgs).union(dunedin_cpgs).union(physage_cpgs)

# 6. Filter out the Intercept rows (catches both "Intercept" and "(Intercept)")
clean_cpgs = {cpg for cpg in all_cpgs if 'Intercept' not in str(cpg)}

print(f"Horvath sites: {len(horvath_cpgs) - 1}") # -1 for intercept
print(f"PhenoAge sites: {len(pheno_cpgs) - 1}")
print(f"DunedinPACE sites: {len(dunedin_cpgs) - 1}")
print(f"PhysAge sites: {len(physage_cpgs) - 1}")
print(f"Total unique clock CpGs for ReadFish: {len(clean_cpgs)}")

# 7. Find Anchor genes using Zhou's Gencode file
print(f"Reading {zhou_gencode} and searching for Anchor Genes...\n")
df_gencode = pd.read_csv(zhou_gencode, sep="\t", compression="gzip")
anchor_mask = df_gencode['geneNames'].fillna('').apply(
    lambda x: any(gene in x.split(';') for gene in anchor_genes)
)
df_anchors = df_gencode[anchor_mask]['probeID']
anchor_cpgs = set(df_anchors)
print(f"Found {len(anchor_cpgs)} CpGs associated with {anchor_genes}\n")

# 8. Merge Clock targets with Quality Control Anchors
print("Loading Coordinates and matching legacy IDs...\n")
df_manifest = pd.read_csv(zhou_manifest, sep="\t", compression="gzip")

# Strip the EPIC v2 suffix (e.g., '_TC21') to match legacy clock IDs
df_manifest['base_cg'] = df_manifest['Probe_ID'].str.split('_').str[0]

df_targets = df_manifest[
    df_manifest['base_cg'].isin(clean_cpgs) | 
    df_manifest['Probe_ID'].isin(anchor_cpgs)
].copy()

# Filter multi-mappers (mapQ_A MUST be 60; mapQ_B can be 60 or NaN)
print("Filtering out multi-mappers and repetitive elements...\n")
df_targets = df_targets[
    (df_targets['mapQ_A'] == 60) &
    (df_targets['mapQ_B'].isna() | (df_targets['mapQ_B'] == 60))
].copy()

# 9. Apply the Latino MAF > 1% / Repetitive Mask
print("🛡️ Applying strict population SNP and repetitive masking...")
df_mask = pd.read_csv(zhou_mask, sep="\t", compression="gzip")

# A probe is bad IF it fails the general structural check (M_general) 
# OR if its specific mask details contain an AMR variant >1% MAF
bad_condition = (df_mask['M_general'] == True) | (df_mask['maskUniq'].fillna('').str.contains('AMR_1pt'))

bad_probes = set(df_mask[bad_condition]['Probe_ID'])
df_final = df_targets[~df_targets['Probe_ID'].isin(bad_probes)].copy()

print(f"   Excluded {len(df_targets) - len(df_final)} problematic positions.")

# 10. Generate and format standard BED file
print("Formatting final target BED file...\n")
df_bed = df_final[['CpG_chrm', 'CpG_beg', 'CpG_end', 'Probe_ID']].copy()

# Ensure coordinates fall within a canonical chormosome
df_bed['chrom_clean'] = df_bed['CpG_chrm'].str.replace('chr', '')
df_bed = df_bed[df_bed['chrom_clean'].isin(valid_chroms)].copy()
df_bed = df_bed.drop(columns=['chrom_clean'])

# Sort chronologically by position
df_bed = df_bed.sort_values(by=['CpG_chrm', 'CpG_beg'])

df_bed['CpG_beg'] = df_bed['CpG_beg'].astype(int)
df_bed['CpG_end'] = df_bed['CpG_end'].astype(int)


df_bed.to_csv(OUTPUT_BED, sep='\t', header=False, index=False)
print(f"\nSUCCESS! Clean ReadFish BED file generated: {OUTPUT_BED} ({len(df_bed)} positions)")
