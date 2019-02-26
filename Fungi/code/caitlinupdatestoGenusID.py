#!/usr/bin/env python
import fungi_stats_helper_functions as helper
import re

import sqlite3
import pandas as pd
import ete3
from ete3 import NCBITaxa



conn = sqlite3.connect(r'../data/refSeqFungiStats.db')
c = conn.cursor()

c.execute("SELECT GENUSTAXID from SPECIESDB where GENUSTAXID IS NOT NULL")
dbquerry = c.fetchall()

ncbi_taxa = NCBITaxa()
for row in dbquerry:
    genusID = row[0]
    OGID = genusID
    name = ncbi_taxa.get_taxid_translator([genusID])
    rank = ncbi_taxa.get_rank(name)
    lineage = ncbi_taxa.get_lineage(genusID)
    nope = ['family', 'order', 'class', 'phylum', 'kingdom'] # These levels are too far
    while((rank[genusID] == 'species' or rank[genusID] == 'species group' or rank[genusID] == 'no rank')):
        if ncbi_taxa.get_rank([lineage[-2]])[lineage[-2]] in nope: #if lineage passes genus, stop
            break
        genusID = lineage[-2] # -1 is the current taxid -2 is the next one (which we want)
        lineage = ncbi_taxa.get_lineage(genusID) #update the lineage
        name = ncbi_taxa.get_taxid_translator([genusID])
        rank = ncbi_taxa.get_rank(name)
    print(rank)
    c.execute("UPDATE SPECIESDB SET GENUSTAXID = ? WHERE GENUSTAXID = ?", (genusID, OGID))
    conn.commit()