#!/bin/bash

wget ftp://ftp.patricbrc.org/RELEASE_NOTES/genome_lineage

grep ";Bacteria;" genome_lineage | awk '{print $1}' > genome_list

for i in `cat genome_list`; do wget -qN "ftp://ftp.patricbrc.org/genomes/$i/$i.fna"; done

rm genome_lineage
rm genome_list
