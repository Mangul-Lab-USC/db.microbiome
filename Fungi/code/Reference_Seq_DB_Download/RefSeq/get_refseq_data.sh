#fungi
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/fungi/assembly_summary.txt
awk -F "\t" '$11=="latest"{print $20}' assembly_summary.txt > ftpdirpaths
awk 'BEGIN{FS=OFS="/";filesuffix="genomic.fna.gz"}{ftpdir=$0;asm=$10;file=asm"_"filesuffix;print ftpdir,file}' ftpdirpaths > ftpfilepaths

while read line;do wget $line;done<ftpfilepaths
