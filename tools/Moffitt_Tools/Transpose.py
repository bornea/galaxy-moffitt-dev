#This program takes any csv file and transposes it

import csv
import sys

infile = sys.argv[1]
outfile = sys.argv[2]
with open(infile) as fin, open(outfile, 'w') as fout:
    rows = csv.reader(fin, delimiter=',', skipinitialspace=True)
    csv.writer(fout, delimiter=',').writerows(zip(*rows))