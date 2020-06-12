# variation_annotation_challenge

This prototype program is a variant annotation tool. The input is a VCF file and the outputs are two csv files with specific information about the variants parsed from the VCF file.

----------------------
Command Line Arguments
----------------------

python variation_tool.py -h
usage: variation_tool.py [-h] [-vcf VCF] [-output OUTPUT] [-api API]

optional arguments:
  -h, --help      show this help message and exit
  -vcf VCF        vcf file
  -output OUTPUT  path to the final annotation output file and the output file name
  -api API        path to the csv table generated for retrieve_API.py and the output
                  file name

Example: python variation_tool.py -vcf /testing/test.vcf -output /testing/output.csv -api /testing/api_out.csv

----------------------
Files Needed
----------------------
VCF file 

----------------------
Disclaimer
----------------------

The second script, retrieve_API.py is not complete. This was my first attempt at extracting data from an API and with unstable internewt at home, I was not able to test it to its full capacity. Currently the path to read in the output file from variation_tool.py is hard coded into the script (line 20) and will need to be changed for each user

