ls ~/scratch/fungi/ensembl/newest_release/ftp.ensemblgenomes.org/pub/fungi/release-44/fasta/ | grep -v -i "collection" | sed 's/^/mv ~\/scratch\/fungi\/ensembl\/newest_release\/ftp.ensemblgenomes.org\/pub\/fungi\/release-44\/fasta\//g' | sed 's/$/\/dna\/\* ~\/scratch\/fungi\/ensembl\/single_files\/release_44\//g' > file_mover.sh

ls ~/scratch/fungi/ensembl/newest_release/ftp.ensemblgenomes.org/pub/fungi/release-44/fasta/ | grep -i "collection" | sed 's/^/mv ~\/scratch\/fungi\/ensembl\/newest_release\/ftp.ensemblgenomes.org\/pub\/fungi\/release-44\/fasta\//g' | sed 's/$/\/\*\/dna\/\* ~\/scratch\/fungi\/ensembl\/single_files\/release_44\//g' >> file_mover.sh

