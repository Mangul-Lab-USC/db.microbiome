#!/usr/bin/env python

def is_mitochnondria(category):
	if category == 'mitochondrial' or category == 'mitochondrion' or category == 'Mt':
		return True
	else:
		return False


def is_plasmid(category):	
	if category == 'plasmid':
		return True
	else:
		return False


def is_contig(category):
		if category == 'contig' or category == 'scaffold' or category == 'sca':
			return True
		else:
			return False

def is_chromosome(category):
	if category == 'chromosome' or category == 'chr':
		return True
	else:
		return False


def determine_sequence_lengths(prev_dna_type, nucleotide_count, chrom_lengths, mt_lengths, plasmid_lengths, contig_lengths):
	if prev_dna_type == "":
		return
	elif prev_dna_type == "chromosome":
		chrom_lengths.append(nucleotide_count)
	elif prev_dna_type == "mitochondria":
		mt_lengths.append(nucleotide_count)
	elif prev_dna_type == "plasmid":
		plasmid_lengths.append(nucleotide_count)
	elif prev_dna_type == "contig":
		contig_lengths.append(nucleotide_count)