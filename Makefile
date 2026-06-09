.DEFAULT_GOAL := help
.PHONY: setup-env update-env build-targets clean

all: setup-env build-targets clean

ENV_NAME = epiclock_env

setup-env:
	 conda env create -f environment.yml || conda env update -f environment.yml --prune
	@echo "\n✅ Environment is ready! Run 'conda activate $(ENV_NAME)' to use it."
update-env:
	conda env update -f environment.yml --prune
	@echo "\n✅ Environment updated successfully!"

build-targets:
	cd BED && bash generate_bed.sh
	@echo "\n✅ BED file generated!"

clean:
	rm -rf BED/EPI* BED/*csv BED/pyaging_data BED/physage_cpgs.txt BED/hg38.chrom.sizes BED/panel_exact_cpgs_padded_5kb.bed

help:
	@echo "Available commands:"
	@echo "  make setup-env     - Create or update the Conda environment"
	@echo "  make build-targets - Run the BED generation pipeline"
	@echo "  make clean         - Remove support files remaining after build-targets"
	@echo "  make all           - Update env, build BED files, and clean up"
