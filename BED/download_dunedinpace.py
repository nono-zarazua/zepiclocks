#!/usr/bin/env python3
import pyaging as pya

# 1. Load the DunedinPACE clock
print("Downloading/Loading DunedinPACE from pyaging...")
logger = pya.logger.Logger('extract_logger')
clock_obj = pya.pred.load_clock('dunedinpace', 'cpu', 'pyaging_data', logger)

# 2. Extract ONLY the 173 target CpGs (ignoring the 19,827 background ones)
cpgs = clock_obj.base_model_features

# 3. Extract the exact coefficients and the intercept
weights = clock_obj.base_model.linear.weight.data[0].tolist()
intercept = clock_obj.base_model.linear.bias.data[0].item()

# 4. Save to a clean CSV
output_file = "dunedinpace_173_weights.csv"
with open(output_file, 'w') as f:
    f.write("CpG,Coefficient\n")
    f.write(f"(Intercept),{intercept}\n")
    for cpg, weight in zip(cpgs, weights):
        f.write(f"{cpg},{weight}\n")

print(f"\nSuccess! Saved 1 intercept and {len(cpgs)} CpGs to {output_file}")
