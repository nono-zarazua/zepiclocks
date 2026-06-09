.PHONY: all run clean

all: run

run:
	cd BED && bash generate_bed.sh

clean:
	rm -rf BED/EPI* BED/*csv BED/pyaging_data BED/physage_cpgs.txt

