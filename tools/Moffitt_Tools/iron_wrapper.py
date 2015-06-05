import os
import sys
import re
import subprocess


input_file = sys.argv[1]
output_file = sys.argv[2]

cmd = r"/home/bornea/libaffy/findmedian --spreadsheet --ignore-weak " + str(input_file) + r" > ./median_file.txt"
os.system(cmd)

cmd2 = r"tail -2 median_file.txt | head -1 | cut -f 4"
median_set = subprocess.check_output(cmd2 ,shell=True)
median_set1 = median_set.strip()

cmd3 = r"/home/bornea/libaffy/iron_generic --norm-iron=" + str(median_set1) +r" --proteomics " + str(input_file) + r" -o " + str(output_file)
print cmd3
os.system(cmd3)