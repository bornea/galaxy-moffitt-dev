"""This program reads in a raw maxquant "Samples Report" output and a user generated
bait file and autoformats it into prey and interaction files for SAINTexpress analysis.
Takes 3 arguments: maxquant file, bait file and Y/N for a prey file"""

import sys
import urllib2
import os

mq_file = sys.argv[1]
cmd = r"Rscript /home/bornea/galaxy_moffitt_dev/tools/Moffitt_Tools/bubblebeam/pre_process_protein_name_set.R " + str(mq_file) 
os.system(cmd)

infile = "./tukeys_output.txt" #maxquant "Samples Report" output
prey = sys.argv[2] # Y or N
make_bait= sys.argv[5]



def bait_create(baits, infile):
    #Takes the Bait specified by the user and makes them into a Bait file and includes a check to make sure they are using valid baits.
    baits = make_bait.split()
    i = 0
    bait_file_tmp = open("bait.txt", "wr")
    order = [] 
    bait_cache = []
    while i < len(baits):
        if baits[i+2] == "true":
            T_C = "C"
        else:
            T_C = "T"
        line1 = baits[i] + "\t" + baits[i+1] + "\t" + T_C + "\n"
        q = open(infile,"r")
        for line2 in q:
           line2 = line2.replace("\"", "")
           line2 = line2.replace(r"Intensity.", "") #R coerces "-" into "." this changes them back and remove Intensity from the Bait names.
           line2 = line2.replace(r".", r"-")
    	   temp = line2.split()
    	   if "mapped_protein" in str(temp):
                #If the bait is in the original file then write to cache it if not exit.
                if baits[i] in temp:
                    number_bait = temp.index(str(baits[i]))
                    number_bait = number_bait - 9
                    bait_cache.append((number_bait, str(line1)))
                else:
                    print "Error: bad bait " + str(baits[i])
                    sys.exit()
           else: 
                pass          			
        i = i + 3
    #Writes cache to file.
    bait_cache.sort()
    for line in bait_cache:
        bait_file_tmp.write(line[1])			
        
    bait_file_tmp.close()  

baitfile = "bait.txt"

class ReturnValue1(object):
    def __init__(self, sequence, gene):
     self.seqlength = sequence
     self.genename = gene
class ReturnValue2(object):
    def __init__(self, getdata, getproteins, getheader):
        self.data = getdata
        self.proteins = getproteins
        self.header = getheader

def main(maxquant_input): 
    bait_create(make_bait, infile)
    make_inter(maxquant_input)
    if prey == 'true':
        make_prey(maxquant_input)
        no_error_inter(maxquant_input)
        os.rename('prey.txt', sys.argv[4])
    elif prey == 'false':
        if os.path.isfile('error proteins.txt') == True:
            no_error_inter(maxquant_input)
        pass
    elif prey != 'true' or 'false':
        sys.exit("Invalid Prey Argument: Y or N")
    os.rename('inter.txt', sys.argv[3])
    os.rename("bait.txt", sys.argv[6])

def get_info(uniprot_accession_in): #get aa lengths and gene name
    error = open('error proteins.txt', 'a+')
    while True:
        i = 0
	try:  
            data = urllib2.urlopen("http://www.uniprot.org/uniprot/" + uniprot_accession_in + ".fasta")
            break
        except urllib2.HTTPError, err:
            i = i + 1
            if i == 50:
                sys.exit("More than 50 errors. Check your file or try again later.")
            if err.code == 404:
                error.write(uniprot_accession_in + '\t' + "Invalid URL. Check protein" + '\n')
                seqlength = 'NA'
                genename = 'NA'
                return ReturnValue1(seqlength, genename)
            elif err.code == 302:
                sys.exit("Request timed out. Check connection and try again.")
            else:
                sys.exit("Uniprot had some other error")
    lines = data.readlines()
    if lines == []:
        error.write(uniprot_accession_in + '\t' + "Blank Fasta" + '\n')
        error.close
        seqlength = 'NA'
        genename = 'NA'
        return ReturnValue1(seqlength, genename)
    if lines != []:
        seqlength = 0
        header = lines[0]
        for line in lines[1:]:
            line = line.replace("\n","") #strip \n or else it gets counted in the length
            seqlength += len(line) 
        if 'GN=' in header:
            lst = header.split('GN=')
            lst2 = lst[1].split(' ')
            genename = lst2[0]
            error.close
            return ReturnValue1(seqlength, genename)
        if 'GN=' not in header:
            genename = 'N/A'
            error.close
            return ReturnValue1(seqlength, genename)
        
def read_maxquant(maxquant_input):
    with open(maxquant_input,'r') as x: #read in maxquant output file
        dupes = []
        for line in x:
            line = line.strip()
            temp = line.split('\t')
            dupes.append(temp)
    header_start = 0            
    header = dupes[header_start]
    for i in header:
        i = i.replace(r"\"", "")
        i = i.replace(r"Intensity.", r"")
        i = i.replace(r".", r"-")
    data = dupes[header_start+1:len(dupes)] #cut off blank line and END OF FILE
    proteins = []
    for protein in data:
        proteins.append(protein[0])
    return ReturnValue2(data, proteins, header)

def read_bait(bait_file):
    with open(bait_file,'r') as x: #read in bait file
        bait = []
        for line in x:
            line = line.strip()
            temp = line.split('\t')
            bait.append(temp)
    return bait

def make_inter(maxquant_input):
    bait = read_bait(baitfile)
    data = read_maxquant(maxquant_input).data
    header = read_maxquant(maxquant_input).header
    start = header.index("mapped_protein") + 1
    proteins = read_maxquant(maxquant_input).proteins
    with open('inter.txt', 'w') as y:
        l = start; a = 0
        for b in bait:
            for lst in data:
                if l == len(header):
                        break
                y.write(b[0] + '\t' + b[1] + '\t' + proteins[a] + '\t' + lst[l] + '\n')
                a+=1
                if a == len(proteins):
                    l += 1; a = 0

def make_prey(maxquant_input):
    proteins = read_maxquant(maxquant_input).proteins
    output_file = open("prey.txt",'w')
    for a in proteins:
        a = a.replace("\n","") #remove \n for input into function
        a = a.replace("\r","") #ditto for \r
        seq = get_info(a).seqlength
        GN = get_info(a).genename
        if seq != 'NA':
            output_file.write(a+"\t"+str(seq)+ "\t" + str(GN) + "\n")
    output_file.close()

def no_error_inter(maxquant_input):
    with open('error proteins.txt', 'rt') as er:
        err = []
        for line in er:
            line = line.strip()
            temp = line.split('\t')
            err.append(temp)
    bait = read_bait(baitfile)
    data = read_maxquant(maxquant_input).data
    header = read_maxquant(maxquant_input).header
    start = header.index("mapped_protein") + 1
    proteins = read_maxquant(maxquant_input).proteins
    errors = []
    for e in err:
        errors.append(e[0])
    with open('inter.txt', 'w') as y:
        l = start; a = 0
        for b in bait:
            for lst in data:
                if l == len(header):
                    break
                if proteins[a] not in errors:
                    y.write(b[0] + '\t' + b[1] + '\t' + proteins[a] + '\t' + lst[l] + '\n')
                a+=1
                if a == len(proteins):
                    l += 1; a = 0
if __name__ == '__main__':
    main(infile)

