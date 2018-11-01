#!/usr/bin/env python

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
    print(list_of_lists)
    return list_of_lists


# This function takes in a list of lists (which is a parsed csv file) and the position of the value that
# you want to be the key, and the position of the value of that key within the sublist, and uses those
# variables to make a dictionary out of the list of lists. For our purposes placek = position of taxID and
# placev = position of the file name.
# returns a dictionary


def make_list_of_lists_into_dictionary(list_of_lists, placek, placev):
    dict = {}
    for i in list_of_lists:
        if not i[placek] in dict.keys():  # make new key
            dict[i[placek]] = [i[placev]]
        else:
            dict[i[placek]] += [i[placev]]
    return dict




# Set up the variables
# The names of the text files that hold the csv styled lists matching taxID's to filenames.
# onek_filename = "/u/home/a/akarlsbe/scratch/fungi/code/1k_taxid_filenames.txt" # This one is a list of directories, so must be treated differently
# ensembl_filename = "/u/home/a/akarlsbe/scratch/fungi/code/ensembl_taxID_filename.txt"
# ncbi_filename = "/u/home/a/akarlsbe/scratch/fungi/code/NCBI_taxID_list.txt"

# onek_filename = "/u/home/a/akarlsbe/scratch/fungi/code/1k_taxid_filenames.txt" # This one is a list of directories, so must be treated differently
ensembl_filename = "/Users/aaronkarlsberg/Desktop/Database_source_code/Compare/Fungus/ensembl_taxID_filename.txt"
ncbi_filename = "/Users/aaronkarlsberg/Desktop/Database_source_code/Compare/Fungus/NCBI_taxID_list.txt"

      

# Use the functions
# make the csv files into list of lists
# onek_csv = make_list_and_parse_lines_from_document(onek_filename, "\t")
ncbi_csv = make_list_and_parse_lines_from_document(ncbi_filename, "\t")
ensembl_csv = make_list_and_parse_lines_from_document(ensembl_filename, "\t")

    # turn the csv lists into dictionaries for easier taxID matching
# reminder: placek = position of taxid and placev = position of filename
# onek_dict = make_list_of_lists_into_dictionary(onek_csv, 1, 0)
ncbi_dict = make_list_of_lists_into_dictionary(ncbi_csv, 0, 2)
ensembl_dict = make_list_of_lists_into_dictionary(ensembl_csv, 1, 0)
# 


for x in ncbi_dict:
	print(x)

# print(ncbi_dict["Settu3_AssemblyScaffolds_Repeatmasked.fasta.gz"])

conn = sqlite3.connect('refSeqBacteriaStats.db')
c = conn.cursor()


def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS SPECIESDB(TAXID INT, DBNAME TEXT, MTDNA INT, SINGLECHROMOSOME INT, SINGLECHROMOSOMELENGTH INT, MULTIPLECHROMOSOMES INT, NUMCHROMOSOMES INT, CONTIG INT, NUMCONTIGS INT, FILEPATH TEXT)")
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

# find . -mindepth 2 -type f -print -exec mv {} . \;




def make_array_of_file_paths():
	filesToParse = []
	# filePathList = "/u/home/a/akarlsbe/scratch/fungi/code/filepaths.list"
	filePathList = "/Users/aaronkarlsberg/Desktop/199/Code/filepaths.list"
	with open(filePathList) as f:
                for line in f:
                        filesToParse.append(line)
	return  filesToParse


# parse specific file and store paramters in seqAttributes
def parse_file(filePath):

	seqAttributes = {
		"TAXID": 0,
		"DBNAME": '',
		"MTDNA": 0,
		"SINGLECHROMOSOME": 0,
		"SINGLECHROMOSOMELENGTH": 0,
		"MULTIPLECHROMOSOMES": 0,
		"NUMCHROMOSOMES": 0,
		"CONTIG": 0,
		"NUMCONTIGS": 0,
		"FILEPATH": ''
		}

	seqAttributes["FILEPATH"] = filePath

# extract DBname from filepath:
	ENSEMBLE = re.search(r'.*/ENSEMBLE/.*', filePath)
	ONEK = re.search(r'.*/1K/.*', filePath)
	NCBI = re.search(r'.*/NCBI/.*', filePath)
	if ENSEMBLE:
		# print("ENSEMBLEEEE")
		seqAttributes["DBNAME"] = "ENSEMBLE"
	if ONEK:
		seqAttributes["DBNAME"] = "1K"
	if NCBI:
		# print("NCBIIIII")
		seqAttributes["DBNAME"] = "NCBI"




# NCBI and ENSEMBLE
	fileName = re.search(r'^(.+)/([^/]+)$', filePath).group(2).strip()+'.gz'

	# print(fileName)
# Gonapodya_prolifera_jel478.Ganpr1.dna.toplevel.fa.gz
# Botdo1_1_AssemblyScaffolds_Repeatmasked.fasta.gz
	# print(fileName)
# 	path = print(fileName.group(1))
# 	name = print(fileName.group(2))


# /u/home/a/akarlsbe/scratch/fungi/NCBI
# GCF_000835555.1_Rhin_mack_CBS_650_93_V1_genomic.fna

	# print(ncbi_dict[fileName.group(2).strip() + '.gz'])

	if fileName in ncbi_dict.keys():
		seqAttributes["TAXID"] = int(ncbi_dict[fileName][0])

	# if fileName in onek_dict.keys():
	# 	seqAttributes["TAXID"] = int(onek_dict[fileName][0])
	if fileName in ensembl_dict.keys():
		seqAttributes["TAXID"] = int(ensembl_dict[fileName][0])
		print(ensembl_dict[fileName])
		print("he;lo")
	return seqAttributes

# 	if key pattern is in filepath



# determine if "MTDNA" is present:

# determine if SINGLE Chrom is present: if present determine length.

# determine if MULTI Chrom are present: if present determine how many.

# determine if CONTIGs are present: if present determine how many.
# 


def populate_tables(filesToParse):
	for filePath in filesToParse:
		# print(filePath)
		SeqAttributes = parse_file(filePath)
		c.execute("INSERT INTO SPECIESDB VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (SeqAttributes["TAXID"], SeqAttributes["DBNAME"], SeqAttributes["MTDNA"], SeqAttributes["SINGLECHROMOSOME"], SeqAttributes["SINGLECHROMOSOMELENGTH"], SeqAttributes["MULTIPLECHROMOSOMES"], SeqAttributes["NUMCHROMOSOMES"], SeqAttributes["CONTIG"], SeqAttributes["NUMCONTIGS"], SeqAttributes["FILEPATH"]))
		conn.commit()
	

# function calls:
create_table()
filesToParse = make_array_of_file_paths()
# print(filesToParse)
populate_tables(filesToParse)
conn.close()