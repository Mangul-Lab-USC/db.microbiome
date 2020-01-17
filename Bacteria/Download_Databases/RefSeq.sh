#!/bin/bash

#bacteria
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/assembly_summary.txt
awk -F "\t" '{print $20}' assembly_summary.txt > ftpdirpaths
awk 'BEGIN{FS=OFS="/";filesuffix="genomic.fna.gz"}{ftpdir=$0;asm=$10;file=asm"_"filesuffix;print ftpdir,file}' ftpdirpaths > ftpfilepaths

while read line;do wget $line;done<ftpfilepaths

mkdir ../text_files

mv ftpfilepaths ../text_files/.
mv ftpdirpaths ../text_files/.
mv assembly_summary.txt ../text_files/.

ls -d "$PWD"/* >> ../text_files/filepaths.list
grep -v "refseq_download.sh" ../text_files/filepaths.list > ../text_files/filepath.list
rm ../text_files/filepaths.list
mv ../text_files/filepath.list ../text_files/filepaths.list
