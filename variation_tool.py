"""
Variant annotation tool 
Tempus Bioinformatics Technical Challenege

Author: Crystal Valdez
Date: June 11, 2020


Notes: 
Created two functions that do similar things:

fetch_DP -  Parses our variant data including the depth of sequence 
coverage at the site of each variant. Uses some pysam utilities.

variation_fetch - Reads the VCF file line-by-line and parses out variant type and
number of reads supporting reference and variant (my best guess being the RO and AO flag
in the FORMAT portion of the VCF). It also calculates the percentage of reads supporting 
variant versus the reference reads.
"""

# Packages to import for vcf analysis
import os
import sys
import argparse
from pysam import VariantFile
import pysam
import pandas as pd
import numpy as np
import requests

# command line arguments for 
parser = argparse.ArgumentParser()

parser.add_argument("-vcf", help="vcf file")
parser.add_argument("-output", help="path to final annotation output file and output file name")
parser.add_argument("-api", help="path to table generated for retrieve_API.py file and output file name ")

args = parser.parse_args()


# setup paths for python program to run
sample_vcf =args.vcf
# output files from functions below
output_csv = args.output
var_for_API = args.api


# read in VCF file
vcf_in = VariantFile(sample_vcf)

def fetch_DP(vcf_file):
	"""
	Read in VCF file using pysam and converts into pandas dataframe
	Creates a csv file to be used for retrieve_API.py
	"""
	chrom_list = []

	for rec in vcf_file:		
		# extract chrom, position, read depth and type for each variation
		#chrom_variant = [rec.chrom, rec.pos, rec.ref, rec.alts[0], rec.info["DP"], rec.info["TYPE"]]
		chrom_variant = [rec.chrom, rec.pos, rec.ref, rec.alts[0], rec.info["DP"]]

		chrom_list.append(chrom_variant)
		#print chrom_variant

	chrom_list = pd.DataFrame(chrom_list)
	#chrom_list.columns = ['chrom', 'position', 'reference', 'alternate', 'read depth', 'variation']
	chrom_list.columns = ['chromosome', 'position', 'reference', 'variant', 'read depth']

	
	# write to file to be used for retrieve_API.py script
	#chrom_list.to_csv('variation_info_for_API.csv', sep=',')
	chrom_list.to_csv(var_for_API,sep=',')

	return chrom_list

print fetch_DP(vcf_in)


def variation_fetch(vcf_file):
	"""
	Reads a VCF line by line extracting out:
	1. Reference allele observation count
	2. Alternate allele observation count
	3. Type of variation - if there is more than one, selects the first one

	Calculates the perecentage of read counts (assuming observation count = read counts)
	"""
	ro_array = []
	ao_array = []
	percent_aoro_array = []
	var_type_array = []

	vcf_handle= open(vcf_file)
	for vline in vcf_handle:
		if vline.startswith("#"):
			continue
		else:
			splits = vline.strip().split()
			#parse out INFO for each variation
			var_info =splits[7]
			
			#parse out FORMAT for each variation
			format_info = splits[9]
			
			# reference allele observation count
			format_ro = format_info.split(":")[4]
			ro_array.append(format_ro)

			# alternate allele observation count
			format_ao = format_info.split(":")[6]
			try:
				format_mult_ao = format_ao.split(",")[0]
				#print "alt allele is " + format_mul_ao
				format_ao = format_mult_ao
				ao_array.append(format_ao)
			except:
				format_ao = format_ao
				ao_array.append(format_ao)


			# calcualte percentage of reads supporting variant versus reference
			# some values are zero so instead of dividing by zero, export just 0
			try:
				percent_ao_ro = float(format_ao)/float(format_ro) * 100
				percent_aoro_array.append("%.2f" % percent_ao_ro)
				#print "%.2f" % percent_ao_ro
			except ZeroDivisionError:
				percent_aoro_array.append(0)
				#print 0

			# extract out type of variation, flag TYPE= 
			# going to select the first variation and proceed with that one
			ex_info = var_info.split(";")[-1]
			if len(ex_info.split(",")) > 1:
				#ex_info = "multiple variations"
				ex_mult_info = ex_info.split(",")[0]
				ex_info = ex_mult_info
				var_type_array.append(ex_info.split("=")[1])
			else:
				ex_info = ex_info
				var_type_array.append(ex_info.split("=")[1])

	#print ro_array, ao_array, percent_aoro_array, var_type_array
	
	# Combine all arrays into a dataframe
	var_df = pd.DataFrame({'reference read count (rrc)':ro_array,'variant read count (vrc)':ao_array,
		'percent vrc/rrc':percent_aoro_array,'variant type':var_type_array},
		columns=['reference read count (rrc)', 'variant read count (vrc)', 'percent vrc/rrc', 'variant type'])
	print var_df
	#var_df.to_csv('variation_output.csv', sep=',')
	var_df.to_csv(output_csv, sep=',')

print variation_fetch(sample_vcf)

# two files created by function above
read_depth_input = pd.read_table(var_for_API, sep=',')
variation_input = pd.read_table(output_csv, sep=',')

#print read_depth_input
#print variation_input


def create_final_table(read_depth,variant_data):
	"""
	Read in two tables created by fetch_DP and variation_fetch and combine for final data frame output
	with the following columns:
	1. chromosome
	2. position
	3. reference
	4. variant
	5. read depth
	6. reference read count (rrc)
	7. variant read count (vrc)
	8. percent vrc/rrc
	9. variant type
	"""
	final_df = pd.merge(read_depth, variant_data)
	final_df = final_df.loc[:, ~final_df.columns.str.contains('^Unnamed')]
	final_df.to_csv(output_csv, sep=',')

	print final_df

print create_final_table(read_depth_input, variation_input)












