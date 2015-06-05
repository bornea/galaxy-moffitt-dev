import sys
import urllib2
import time
uniprot_file = open(sys.argv[1],'r')
output_file = open(sys.argv[2],'w')

def get_seq_length(uniprot_accession_in):
    while True:
        i = 0
	try:  
            data = urllib2.urlopen("http://www.uniprot.org/uniprot/" + uniprot_accession_in + ".fasta")
	    break # Keep trying to get the data until it works
        except urllib2.HTTPError, err:
            i = i + 1
            if i == 50:
                sys.exit("More than 50 errors. Check your file or try again later.")
            if err.code == 404:
                print "Invalid URL; trying again"
            elif err.code == 302:
                print "Request timed out; trying again"
            else:
                "Uniprot returned some other error"
    lines = data.readlines()[1:] #skip the first line which contains non-sequence info
    length = 0
    for line in lines:
        line = line.replace("\n","") #strip \n or else it gets counted in the length
        length = length + len(line) 
    return length

for id in uniprot_file:
    id = id.replace("\n","") #remove \n for input into function or else it isn't formatted correctly
    id = id.replace("\r","") #ditto for \r
    output_file.write(id+"\t"+str(get_seq_length(id))+"\n")

uniprot_file.close()
output_file.close()
print 'Done!'
