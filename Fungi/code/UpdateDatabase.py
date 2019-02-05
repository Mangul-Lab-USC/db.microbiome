#!/usr/bin/env python
import fungi_stats_helper_functions as helper
import sqlite3
import re
import csv
import ete3
from ete3 import NCBITaxa




# added STRAINTAXID Column
# changed STRAIN column to STRAINNAME 
# added GENUSNAME and GENUSTAXID columns
# changed TAXID column name SPECIESTAXID

# conn = sqlite3.connect('/Users/aaronkarlsberg/Desktop/199/db.microbiome/Fungi/data/refSeqFungiStats.db')
# c = conn.cursor()

# c.execute("CREATE TABLE IF NOT EXISTS SPECIESDB(TAXID INT, GENUSNAME TEXT, SPECIESNAME TEXT, STRAIN TEXT, DBNAME TEXT, FILEPATH TEXT, chromosome_count INT, avg_length_chromosomes INT, max_length_chromosomes INT, min_length_chromosomes INT, contig_count INT, avg_length_contig INT, max_length_contig INT, min_length_contig INT, mtDNA_count INT, avg_length_mtDNA INT, max_length_mtDNA INT, min_length_mtDNA INT, plasmid_count INT, avg_length_plasmids INT, max_length_plasmids INT, min_length_plasmids INT)")
# conn.commit()	


# c.execute("ALTER TABLE SPECIESDB RENAME TO TMP")


# c.execute("CREATE TABLE IF NOT EXISTS SPECIESDB(GENUSTAXID INT, GENUSNAME TEXT, SPECIESTAXID INT, SPECIESNAME TEXT, STRAINTAXID INT, STRAINNAME TEXT, DBNAME TEXT, FILEPATH TEXT, chromosome_count INT, avg_length_chromosomes INT, max_length_chromosomes INT, min_length_chromosomes INT, contig_count INT, avg_length_contig INT, max_length_contig INT, min_length_contig INT, mtDNA_count INT, avg_length_mtDNA INT, max_length_mtDNA INT, min_length_mtDNA INT, plasmid_count INT, avg_length_plasmids INT, max_length_plasmids INT, min_length_plasmids INT)")


# RUN THIS CODE IN terminal:
# INSERT INTO SPECIESDB(GENUSNAME, SPECIESTAXID, SPECIESNAME, STRAINNAME, DBNAME, FILEPATH, chromosome_count, avg_length_chromosomes, max_length_chromosomes, min_length_chromosomes, contig_count, avg_length_contig, max_length_contig, min_length_contig, mtDNA_count, avg_length_mtDNA, max_length_mtDNA, min_length_mtDNA, plasmid_count, avg_length_plasmids, max_length_plasmids, min_length_plasmids) 
# SELECT GENUSNAME, TAXID, SPECIESNAME, STRAIN, DBNAME, FILEPATH, chromosome_count, avg_length_chromosomes, max_length_chromosomes, min_length_chromosomes, contig_count, avg_length_contig, max_length_contig, min_length_contig, mtDNA_count, avg_length_mtDNA, max_length_mtDNA, min_length_mtDNA, plasmid_count, avg_length_plasmids, max_length_plasmids, min_length_plasmids 
# FROM TMP;


# =================



# pd.read_sql_query(f"UPDATE SPECIESDB WHERE SPECIESTAXID = {SPECIESTAXID} WITH {newSPECIESTAXID}", cnx)

# This code does the following:
# ensures that species level SPECIESTAXIDs are associated with species, and strain SPECIESTAXID with strain.
# uses ncbi naming scheme to ensure all identical genus, species, and strains have consistent names.
# cursor.execute('''UPDATE books SET price = ? WHERE id = ?''', (newPrice, book_id))
# c.execute("INSERT INTO SPECIESDB VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (seqAttributes["TAXID"], seqAttributes["GENUSNAME"], seqAttributes["SPECIESNAME"], seqAttributes["STRAIN"], seqAttributes["DBNAME"], seqAttributes["FILEPATH"], seqAttributes["chromosome_count"], seqAttributes["avg_length_chromosomes"], seqAttributes["max_length_chromosomes"], seqAttributes["min_length_chromosomes"], seqAttributes["contig_count"], seqAttributes["avg_length_contig"], seqAttributes["max_length_contig"], seqAttributes["min_length_contig"], seqAttributes["mtDNA_count"], seqAttributes["avg_length_mtDNA"], seqAttributes["max_length_mtDNA"], seqAttributes["min_length_mtDNA"], seqAttributes["plasmid_count"], seqAttributes["avg_length_plasmids"], seqAttributes["max_length_plasmids"], seqAttributes["min_length_plasmids"]))


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
	conn = sqlite3.connect('/Users/aaronkarlsberg/Desktop/199/db.microbiome/Fungi/data/new_schema_b4_fungiDB/newSchema_with_updates_no_fungidb/newSchema_b4_fungiDB1.db')
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

# # Local:
# Make copies of database, convert to proper schema, and make copies again before running this code!

# DB: oldschemaNOfungidb
# DB: withFUNGIDBOLDSCHEMA
# DB: withFUNGIDBNEWSCHEMA
# DB: withFUNGIDBNEWSHCEMAANDTAXIDU
# Hoffman:
# conn = sqlite3.connect('/u/home/a/akarlsbe/scratch/db.microbiome/Fungi/data/refSeqFungiStats.db')
UPDATE_TAXIDS_AND_NAMES()

