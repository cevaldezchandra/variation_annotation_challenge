"""
Retrieve variant information from Broad Institute ExAC Project API: 
http://exac.hms.harvard.edu/

Tempus Bioinformatics Technical Challenege

Author: Crystal Valdez
Date: June 11, 2020

Disclaimer: This was my first attempt at extracting data from an API and with unstable
internewt at home, I was not able to test it to its full capacity.
"""


import pandas as pd
import requests
import json

#file to read in for variation info
var_for_API =  "/Users/crystalvaldez/Dropbox/Interviews/Tempus/variation_info_for_API.xls"

# Read in data frame created with variation_tool.py
var = pd.read_table(var_for_API, sep='\t')
print list(var.columns)

# Add a column to the dataframe that is formatted as so: CHROMOSOME-POSITION-REFERENCE-VARIANT
var['API format'] = var.apply(lambda x:'%s-%s-%s-%s' % (x['chrom'],x['position'],x['reference'],x['alternate']),axis=1)


api_input = var['API format']
print api_input

### API setup
request = requests.get('http://exac.hms.harvard.edu/')
print(request.status_code) # if we get a 200, we're good to go!

# Loop through all variant formatted for http://exac.hms.harvard.edu
api_info_store = []

for i in range(len(var)):
	api_info = var.loc[i, "API format"]
	print api_info
	api_request = requests.get('http://exac.hms.harvard.edu/rest/variant/' + api_info
	api_info_store.append(api_request)

"""
Steps I would take next:
1. Final api_info_store array would then be converted to a data frame
2. Select allele frequency of variant from this data 
3. Parse any additional information about variant (i.e. prevalance in individuals, non-coding exons, etc.)
4. Append dataframe to final one created by variation_tool.py
"""
