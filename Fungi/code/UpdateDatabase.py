#!/usr/bin/env python
import fungi_stats_helper_functions as helper
import sqlite3
import re
import csv
import ete3
from ete3 import NCBITaxa


def get_name(taxId):
	ncbi_taxa = NCBITaxa()
	name_dict = ncbi_taxa.get_taxid_translator([taxId])
	for taxid, name in name_dict.items():
		# print(name)
		return name


def get_rank(taxId):
	ncbi_taxa = NCBITaxa()
	rank_dict = ncbi_taxa.get_rank([taxId])
	for taxid, rank in rank_dict.items():
		# print(rank)
		return rank



def get_lineage(taxId):
	ncbi_taxa = NCBITaxa()
	lineage = ncbi_taxa.get_lineage(taxId)
	return lineage

def UPDATE_TAXIDS_AND_NAMES():
	conn = sqlite3.connect('/Users/aaronkarlsberg/Desktop/199/db.microbiome/Fungi/data/refSeqFungiStatsWithFUNGIDB_NEW_SCHEMA_AND_TAXID_UPDATES.db')
	c = conn.cursor()
	c.execute("SELECT SPECIESTAXID from SPECIESDB")
	speciesTaxIds = c.fetchall()
	for row in speciesTaxIds:
		taxId = row[0]
		ncbi_version_name = get_name(taxId)	
		rank = get_rank(taxId)
		if rank == 'genus':
			print('genus')
			c.execute("UPDATE SPECIESDB set GENUSNAME = ?, GENUSTAXID = ?, SPECIESTAXID = 0  WHERE SPECIESTAXID = ?", (ncbi_version_name, taxId, taxId))
			conn.commit()
		if rank == 'species':
			print('species')
			c.execute("UPDATE SPECIESDB set SPECIESNAME = ? WHERE SPECIESTAXID = ?", (ncbi_version_name, taxId))
			conn.commit()
			genusID = get_lineage(taxId)[-2]
			genusName = get_name(genusID)
			c.execute("UPDATE SPECIESDB set GENUSTAXID = ?, GENUSNAME = ? WHERE SPECIESTAXID = ?", (genusID, genusName, taxId))
			conn.commit()
		if rank == 'no rank':
			print('no rank')
			c.execute("UPDATE SPECIESDB set STRAINNAME = ?, STRAINTAXID = ?, SPECIESTAXID = 0 WHERE SPECIESTAXID = ?", (ncbi_version_name, taxId, taxId))
			conn.commit()
			speciesID = get_lineage(taxId)[-2]
			speciesName = get_name(speciesID)
			genusID = get_lineage(taxId)[-3]
			genusName = get_name(genusID)
			c.execute("UPDATE SPECIESDB set SPECIESTAXID = ?, SPECIESNAME = ?, GENUSTAXID = ?, GENUSNAME = ? WHERE STRAINTAXID = ?", (speciesID, speciesName, genusID, genusName, taxId))
			conn.commit()
			# # # # # # # # # # #  error handling # # # # # # # # # # # #
			if get_rank(genusID) != 'genus':
				print("expected rank failed" + get_rank(genusID))
			# # # # # # # # # # # #  error handling # # # # # # # # # # # #
	conn.close()

UPDATE_TAXIDS_AND_NAMES()
# # Local:
# Make copies of database, convert to proper schema, and make copies again before running this code!

# DB: oldschemaNOfungidb
# DB: withFUNGIDBOLDSCHEMA
# DB: withFUNGIDBNEWSCHEMA
# DB: withFUNGIDBNEWSHCEMAANDTAXIDU


