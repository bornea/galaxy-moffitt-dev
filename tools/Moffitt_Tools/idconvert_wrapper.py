import os
import sys

input_file = open(sys.argv[1],'r')
output_file = sys.argv[2]
output_format = sys.argv[3]

if output_format == "mzid":
	cmd = "idconvert " + str(sys.argv[1])
	os.system(cmd)
	open('spectra.mzid')
	os.rename('spectra.mzid', str(sys.argv[2])) 
elif output_format == "pepxml":
	cmd = "idconvert " + str(sys.argv[1]) + " --pepXML"
	os.system(cmd)
	open('spectra.pepXML')
	os.rename('spectra.pepXML', str(sys.argv[2])) 
elif output_format == "text":
	cmd = "idconvert " + str(sys.argv[1]) + " --text"
	os.system(cmd)
	open('spectra.txt')
	os.rename('spectra.txt', str(sys.argv[2])) 
	


