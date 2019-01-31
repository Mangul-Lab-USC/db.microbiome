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


def UPDATE_TAXIDS_AND_NAMES(conn, c):
	speciesTaxIds = c.execute("SELECT SPECIESTAXID from SPECIESDB")
	ncbi_taxa = NCBITaxa()
	for index, row in speciesTaxIds.iterrows():
		taxId = row["SPECIESTAXID"]
		ncbi_version_name = ncbi_taxa.get_taxid_translator(taxId)
		rank = ncbi_taxa.get_rank(ncbi_version_name)
		if rank == 'genus':
			c.execute("UPDATE SPECIESDB set GENUSNAME = {ncbi_version_name}, GENUSTAXID = {taxId}, SPECIESTAXID = 0,  WHERE SPECIESTAXID = {taxId}")
			conn.commit()
		if rank == 'species':
			c.execute("UPDATE SPECIESDB set SPECIESNAME = {ncbi_version_name} WHERE SPECIESTAXID = {taxId}")
			conn.commit()
			genusID = ncbi_taxa.get_lineage(taxId)[-2]
			genusName = ncbi_taxa.get_taxid_translator(genusID)
			c.execute("UPDATE SPECIESDB set GENUSTAXID = {genusID}, GENUSNAME = {genusName} WHERE SPECIESTAXID = {taxId}")
			conn.commit()
		if rank == 'no rank':
			c.execute("UPDATE SPECIESDB set STRAINNAME = {ncbi_version_name}, STRAINTAXID = {taxId}, SPECIESTAXID = 0, WHERE SPECIESTAXID = {taxId}")
			conn.commit()
			speciesID = ncbi_taxa.get_lineage(taxId)[-2]
			speciesName = ncbi_taxa.get_taxid_translator(speciesID)
			genusID = ncbi_taxa.get_lineage(taxId)[-3]
			genusName = ncbi_taxa.get_taxid_translator(genusID)
			c.execute("UPDATE SPECIESDB set SPECIESTAXID = {speciesID}, SPECIESNAME = {speciesName}, GENUSTAXID = {genusID}, GENUSNAME = {genusName} WHERE STRAINTAXID = {taxId}")
			conn.commit()
			# # # # # # # # # # # #  error handling # # # # # # # # # # # #
			if ncbi_taxa.get_rank(genusID) != 'genus':
				print("expected rank failed")
			# # # # # # # # # # # #  error handling # # # # # # # # # # # #

conn = sqlite3.connect('/Users/aaronkarlsberg/Desktop/199/db.microbiome/Fungi/data/refSeqFungiStats.db')
c = conn.cursor()
UPDATE_TAXIDS_AND_NAMES(conn, c)
conn.close()


