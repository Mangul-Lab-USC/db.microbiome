#!/usr/bin/env python
import fungi_stats_helper_functions as helper
import sqlite3
import re

# This function was built to take in csv files and turn them into lists of lists, where every element of the
# list is an individual row of the csv file and ever element of the sublist are the entries for each column
# of that particular row
# returns this list of lists


def make_list_and_parse_lines_from_document(filename, parse_by):
 
    f = open(filename)
    list_of_lists = []
    for l in f:
        line = l.strip().split(parse_by)
        # print(line)
        list_of_lists += [line]
    f.close()
    # print(list_of_lists)
    return list_of_lists

# This function takes in a list of lists (which is a parsed csv file) and the position of the value that
# you want to be the key, and the position of the value of that key within the sublist, and uses those
# variables to make a dictionary out of the list of lists. For our purposes placek = position of taxID and
# placev = position of the file name.
# returns a dictionary


def make_list_of_lists_into_dictionary(list_of_lists, placek, placev, placet):
    dict = {}
    for i in list_of_lists:
        if not i[placek] in dict.keys():  # make new key
            dict[i[placek]] = [i[placev]]
        else:
        	dict[i[placek]] += [i[placev]]
        dict[i[placek]] += [i[placet]]
        # print(i[placet])
    return dict

# Set up the variables
# The names of the text files that hold the csv styled lists matching taxID's to filenames.
# onek_filename = "/u/home/a/akarlsbe/scratch/fungi/code/updated_onek_csv.txt" # This one is a list of directories, so must be treated differently
# ensembl_filename = "/u/home/a/akarlsbe/scratch/fungi/code/updated_ensemble_csv.txt"
# ncbi_filename = "/u/home/a/akarlsbe/scratch/fungi/code/NCBI_taxID_list.txt"
# onek_filename = "/u/home/a/akarlsbe/scratch/fungi/code/1k_taxid_filenames.txt" # This one is a list of directories, so must be treated differently
fungiDB_filename = "/u/home/a/akarlsbe/scratch/db.microbiome/Fungi/code/Fungidb_csv.txt"

# onek_filename = '/Users/aaronkarlsberg/Desktop/db.microbiome/Code/updated_onek_csv.txt'
# ensembl_filename = "/Users/aaronkarlsberg/Desktop/db.microbiome/Code/updated_ensembl_csv.txt"
# ncbi_filename = "/Users/aaronkarlsberg/Desktop/db.microbiome/Code/NCBI_taxID_list.txt"
# fungiDB_filename = "/Users/aaronkarlsberg/Desktop/db.microbiome/Code/Fungidb_csv.txt"



# Use the functions
# make the csv files into list of lists
# onek_csv = make_list_and_parse_lines_from_document(onek_filename, "\t")
# ncbi_csv = make_list_and_parse_lines_from_document(ncbi_filename, "\t")
# ensembl_csv = make_list_and_parse_lines_from_document(ensembl_filename, "\t")
fungiDB_csv = make_list_and_parse_lines_from_document(fungiDB_filename, "\t")
    # turn the csv lists into dictionaries for easier taxID matching
# # reminder: placek = position of taxid and placev = position of filename
# onek_dict = make_list_of_lists_into_dictionary(onek_csv, 1, 0, 3)
# ncbi_dict = make_list_of_lists_into_dictionary(ncbi_csv, 0, 2, 1)
# ensembl_dict = make_list_of_lists_into_dictionary(ensembl_csv, 1, 0, 2)
fungiDB_dict = make_list_of_lists_into_dictionary(fungiDB_csv, 3, 1, 0)



# print(ncbi_dict.keys())
# print(onek_dict.keys())
# print(ensembl_dict.keys())

# print(ncbi_dict)
# print(ensembl_dict)

# print(ncbi_dict["Settu3_AssemblyScaffolds_Repeatmasked.fasta.gz"])

conn = sqlite3.connect('refSeqFungiStats.db')
c = conn.cursor()


def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS SPECIESDB(TAXID INT, GENUSNAME TEXT, SPECIESNAME TEXT, STRAIN TEXT, DBNAME TEXT, FILEPATH TEXT, chromosome_count INT, avg_length_chromosomes INT, max_length_chromosomes INT, min_length_chromosomes INT, contig_count INT, avg_length_contig INT, max_length_contig INT, min_length_contig INT, mtDNA_count INT, avg_length_mtDNA INT, max_length_mtDNA INT, min_length_mtDNA INT, plasmid_count INT, avg_length_plasmids INT, max_length_plasmids INT, min_length_plasmids INT)")
	conn.commit()	

# Make function that reads each reference sequence file in each databse and:
# - looks at taxid, which database, if there is MTDNA, singlechromosme, contig etc and inserts into table.
# make a function that separates mitchondrial dna

# make an array of file paths to parse.

# Run in terminal to compile list of filepaths for unzipped gzfiles. 
# ls -d "$PWD"/* >> /u/home/a/akarlsbe/scratch/fungi/code/filepaths.list
# 	onek_path = "/u/home/a/akarlsbe/scratch/fungi/1K" # leads to the list of directories
# 	ensembl_path = "/u/home/a/akarlsbe/scratch/fungi/ENSEMBLE"
#	ncbi_path = "/u/home/a/akarlsbe/scratch/fungi/NCBI"
# moves all files in subdirectories of depth 2 into current directory.
# find . -mindepth 2 -type f -print -exec mv {} . \;





# ls -d "$PWD"/* >> /Users/aaronkarlsberg/Desktop/db.microbiome/Code/aaron.list

def make_array_of_file_paths():
	filesToParse = []
	# filePathList = "/u/home/a/akarlsbe/scratch/fungi/code/filepaths.list"
	filePathList = "/Users/aaronkarlsberg/Desktop/db.microbiome/Code/filepaths.list"
	with open(filePathList) as f:
                for line in f:
                        filesToParse.append(line)
	return  filesToParse


# parse specific file and store paramters in seqAttributes
def parse_file(filePath):
	nucleotide_count = 0
	prev_dna_type = ""
	chrom_lengths = [] 
	mt_lengths = [] 
	plasmid_lengths = [] 
	contig_lengths = []


	seqAttributes = {
		"TAXID": 0,
		"GENUSNAME": '',
		"SPECIESNAME": '',
		"STRAIN": '',
		"DBNAME": '',
		"FILEPATH": '',
		"chromosome_count": 0,
		"avg_length_chromosomes": 0,
		"max_length_chromosomes": 0,
		"min_length_chromosomes": 0,

		"contig_count": 0,
		"avg_length_contig": 0,
		"max_length_contig": 0,
		"min_length_contig": 0,

		"mtDNA_count": 0,
		"avg_length_mtDNA": 0,
		"max_length_mtDNA": 0,
		"min_length_mtDNA": 0,

		"plasmid_count": 0,
		"avg_length_plasmids": 0,
		"max_length_plasmids": 0,
		"min_length_plasmids": 0
		}

	seqAttributes["FILEPATH"] = filePath

# extract DBname from filepath:
	ENSEMBLE = re.search(r'.*/ENSEMBLE/.*', filePath)
	ONEK = re.search(r'.*/1K/.*', filePath)
	NCBI = re.search(r'.*/NCBI/.*', filePath)
	FUNGIDB = re.search(r'.*/FUNGIDB/.*', filePath)
	if ENSEMBLE:
		# print("ENSEMBLEEEE")
		seqAttributes["DBNAME"] = "ENSEMBLE"
	if ONEK:
		seqAttributes["DBNAME"] = "1K"
	if NCBI:
		seqAttributes["DBNAME"] = "NCBI"
	if FUNGIDB:
		seqAttributes["DBNAME"] = "FUNGIDB"



# modify filename from dictionaries to compare. add gz
	fileName = re.search(r'^(.+)/([^/]+)$', filePath).group(2).strip()+'.gz'



	if fileName in fungiDB_dict.keys():
		seqAttributes["TAXID"] = int(fungiDB_dict[fileName][0])
		# print(fungiDB_dict[fileName][1])
		seqAttributes["GENUSNAME"] = fungiDB_dict[fileName][1].split(' ', 1)[0].lower()
		if len(fungiDB_dict[fileName][1].split(' ', 1)) > 1:
			seqAttributes["SPECIESNAME"] = fungiDB_dict[fileName][1].split(' ', 1)[1].lower()
		else:
			seqAttributes["SPECIESNAME"] = "species name not provided"





	# extract TAXID FROM DICTIONARIES
	if fileName in ncbi_dict.keys():
		seqAttributes["TAXID"] = int(ncbi_dict[fileName][0])
		# print(ncbi_dict[fileName][1])
		seqAttributes["GENUSNAME"] = ncbi_dict[fileName][1].split(' ', 1)[0].lower()
		if len(ncbi_dict[fileName][1].split(' ', 1)) > 1:
			seqAttributes["SPECIESNAME"] = ncbi_dict[fileName][1].split(' ', 1)[1].lower()
		else:
			seqAttributes["SPECIESNAME"] = "species name not provided"


	if fileName in onek_dict.keys():
		seqAttributes["TAXID"] = int(onek_dict[fileName][0])
		# print(onek_dict[fileName][1])
		seqAttributes["GENUSNAME"] = onek_dict[fileName][1].split(' ', 1)[0].lower()
		if len(onek_dict[fileName][1].split(' ', 1)) > 1:
			seqAttributes["SPECIESNAME"] = onek_dict[fileName][1].split(' ', 1)[1].lower()
		else:
			seqAttributes["SPECIESNAME"] = "species name not provided"

	if fileName in ensembl_dict.keys():
		seqAttributes["TAXID"] = int(ensembl_dict[fileName][0])
		# print(ensembl_dict[fileName][1].split(' ', 1)[0].lower())
		# print(ensembl_dict[fileName][1].split(' ', 1)[1].lower())
		seqAttributes["GENUSNAME"] = ensembl_dict[fileName][1].split(' ', 1)[0].lower()
		if len(ensembl_dict[fileName][1].split(' ', 1)) > 1:
			seqAttributes["SPECIESNAME"] = ensembl_dict[fileName][1].split(' ', 1)[1].lower()
		else:
			seqAttributes["SPECIESNAME"] = "species name not provided"
	




# open individual sequence file and determine following attributes:
	# 	with open(filePath.strip()) as f:
	# 		for line in f:
	# # determine what type of dna is present in following sequence and increment count of sequences for dna type in file.: 
	# 			dnaCategories = re.findall(r"Mt", line) # where we dont ignore case for mt 
	# 			dnaCategories += re.findall(r"mitochondrial|mitochondrion|plasmid|contig|scaffold|chromosome|sca|chr", line, re.I)
	# 			chromosome = False
	# 			plasmid = False
	# 			mitochondria = False
	# 			contig = False
	# 			# print("HELLOOOO")

	# # determine all categories which are marked true. loop through categories array.
	# 			for category in dnaCategories:
	# 				if helper.is_mitochnondria(category):
	# 					mitochondria = True
	# 					# print("mitchondria")
	# 				elif helper.is_plasmid(category):
	# 					plasmid = True
	# 					# print("plasmid")
	# 				elif helper.is_contig(category):
	# 					contig = True
	# 					# print("contig")
	# 				elif helper.is_chromosome(category):
	# 					chromosome = True
	# 					# print("chromosome")

	# 	# mark sequence according to priority as follows. Chromosome is last bc it is used in name even when the sequence is only a contig or scaffold.
	# 	# mark line number and compare current count of nucleotides to 
	# 			if mitochondria:
	# 				seqAttributes["mtDNA_count"] += 1
	# 				helper.determine_sequence_lengths(prev_dna_type, nucleotide_count, chrom_lengths, mt_lengths, plasmid_lengths, contig_lengths)
	# 				prev_dna_type = 'mitochondria'
	# 				nucleotide_count = 0
	# 			elif plasmid:
	# 				seqAttributes["plasmid_count"] += 1
	# 				helper.determine_sequence_lengths(prev_dna_type, nucleotide_count, chrom_lengths, mt_lengths, plasmid_lengths, contig_lengths)
	# 				prev_dna_type = 'plasmid'
	# 				nucleotide_count = 0

	# 			elif contig:
	# 				seqAttributes["contig_count"] += 1
	# 				helper.determine_sequence_lengths(prev_dna_type, nucleotide_count, chrom_lengths, mt_lengths, plasmid_lengths, contig_lengths)
	# 				prev_dna_type = 'contig'
	# 				nucleotide_count = 0
	# 			elif chromosome:
	# 				seqAttributes["chromosome_count"] += 1
	# 				helper.determine_sequence_lengths(prev_dna_type, nucleotide_count, chrom_lengths, mt_lengths, plasmid_lengths, contig_lengths)
	# 				prev_dna_type = 'chromosome'
	# 				nucleotide_count = 0
	# 				# if none of above conditions are satisfied, then line is a sequence of nucleotides so add the length of that line to nucleotide count to determine next seq length.
	# 			else:
	# 				nucleotide_count += len(line)
	# 				# print(nucleotide_count)
	# 				# print("hello")

	# 			# print("hello")
	# 	# sort arrays containing lengths of each seqeuence. Determine min, max and avg lengths.
	# 	if len(chrom_lengths) >= 1:	
	# 		chrom_lengths.sort()
	# 		sum_chrom_lengths = 0
	# 		seqAttributes["min_length_chromosomes"] = chrom_lengths[0]
	# 		seqAttributes["max_length_chromosomes"] = chrom_lengths[-1]
	# 		for lengths in chrom_lengths:
	# 			sum_chrom_lengths += lengths
	# 		seqAttributes["avg_length_chromosomes"] = sum_chrom_lengths / seqAttributes["chromosome_count"]

	# 	if len(mt_lengths) >= 1:
	# 		mt_lengths.sort()
	# 		sum_mt_lengths = 0
	# 		seqAttributes["min_length_mtDNA"] = mt_lengths[0]
	# 		seqAttributes["max_length_mtDNA"] = mt_lengths[-1]
	# 		for lengths in mt_lengths:
	# 			sum_mt_lengths += lengths
	# 		seqAttributes["avg_length_mtDNA"] = sum_mt_lengths / seqAttributes["mtDNA_count"]

	# 	if len(plasmid_lengths) >= 1:
	# 		plasmid_lengths.sort()
	# 		sum_plasmid_lengths = 0
	# 		seqAttributes["min_length_plasmids"] = plasmid_lengths[0]
	# 		seqAttributes["max_length_plasmids"] = plasmid_lengths[-1]
	# 		for lengths in plasmid_lengths:
	# 			sum_plasmid_lengths += lengths
	# 		seqAttributes["avg_length_plasmids"] = sum_plasmid_lengths / seqAttributes["plasmid_count"]


	# 	if len(contig_lengths) >= 1:
	# 		contig_lengths.sort()
	# 		sum_contig_lengths = 0
	# 		# print(contig_lengths)
	# 		seqAttributes["min_length_contig"] = contig_lengths[0]
	# 		seqAttributes["max_length_contig"] = contig_lengths[-1]
	# 		for lengths in contig_lengths:
	# 			sum_contig_lengths += lengths
	# 		seqAttributes["avg_length_contig"] = sum_contig_lengths / seqAttributes["contig_count"]

	# print(seqAttributes)
	return seqAttributes


def populate_tables(filesToParse):
	for filePath in filesToParse:
		# print(filePath)
		seqAttributes = parse_file(filePath)																						

		c.execute("INSERT INTO SPECIESDB VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (seqAttributes["TAXID"], seqAttributes["GENUSNAME"], seqAttributes["SPECIESNAME"], seqAttributes["STRAIN"], seqAttributes["DBNAME"], seqAttributes["FILEPATH"], seqAttributes["chromosome_count"], seqAttributes["avg_length_chromosomes"], seqAttributes["max_length_chromosomes"], seqAttributes["min_length_chromosomes"], seqAttributes["contig_count"], seqAttributes["avg_length_contig"], seqAttributes["max_length_contig"], seqAttributes["min_length_contig"], seqAttributes["mtDNA_count"], seqAttributes["avg_length_mtDNA"], seqAttributes["max_length_mtDNA"], seqAttributes["min_length_mtDNA"], seqAttributes["plasmid_count"], seqAttributes["avg_length_plasmids"], seqAttributes["max_length_plasmids"], seqAttributes["min_length_plasmids"]))
		conn.commit()

# function calls:
create_table()

filesToParse = make_array_of_file_paths()

# test on one fasta fungi file
# filesToParse = ["/Users/aaronkarlsberg/Desktop/199/Code/fungifastas/Allomyces_macrogynus_atcc_38327.A_macrogynus_V3.dna.toplevel.fa"]

# print(filesToParse)
populate_tables(filesToParse)
conn.close()


