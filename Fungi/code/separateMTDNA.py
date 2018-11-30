#!/usr/bin/env python
import re


def make_array_of_file_paths():
	filesToParse = []
	filePathList = "/u/home/a/akarlsbe/scratch/fungi/code/filepaths.list"
	with open(filePathList) as f:
             for line in f:
                        filesToParse.append(line)
	return  filesToParse


# determine if there is mtdna
def mtdna_present(fileContents):
		MTDNA = re.search(r'mitchondria', fileContents)
		if MTDNA:
			return True


# if there is then construct new mtdna file name and path with DB, taxID and mtdnaLabel
def construct_new_mtdna_file_Path(fileContents, filePath):
	# determine database:
	newFilePath = re.match( r'^.*/', filePath)
	newFilePath += "mtdna"
	ENSEMBLE = re.search(r'ENSEMBLE', filePath)
	ONEK = re.search(r'1K', filePath)
	NCBI = re.search(r'NCBI', filePath)
	if ENSEMBLE:
		newFilePath += "_ENSEMBLE_"
	if ONEK:
		newFilePath += "_1K_"
	if NCBI:
		newFilePath += "_NCBI_"
	# determin taxID:


def output_mitcondrial_dna_to_new_file(contents, newFilePath):
			newFile = open("{newFilePath}".format(newFilePath), "w")
			newFile.write()
			newFile.close()


# delete mtdna from original file.
def remove_mitcondrial_dna_from_original_file(filePath):
			originalFile =  open("{filePath}".format(filePath), "w")
			originalFile.write()
			originalFile.close()



# if mitchondria then write remainder of file to new file. delete mitochondria from current file.



def mtDNA_handler(filePaths):
	for filePath in filePaths:
		originalFile = open("{filePath}".format(filePath), "r")
		fileContents = originalFile.read()
	if mtdna_present(fileContents):
		newFileName = construct_new_mtdna_file_Path(fileContents, filePath)
		output_mitcondrial_dna_to_new_file(fileContents, newFileName)
		originalFile.close()
		remove_mitcondrial_dna_from_original_file(filePath)


# function calls
filePaths = make_array_of_file_paths()
mtDNA_handler(filePaths)