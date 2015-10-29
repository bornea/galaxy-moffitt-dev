import os 
import sys
import time


list_file = sys.argv[1]
prey_file = sys.argv[2]
crapome = sys.argv[3]
color = sys.argv[4]
label = sys.argv[5]
cutoff = sys.argv[6]
mq_sc = sys.argv[7]
output_file_name = sys.argv[8]
bub_zoom_NSAF = sys.argv[9]
bub_zoom_SAINT =sys.argv[10]
bub_SAINT = sys.argv[11]
bub_NSAF = sys.argv[12]

if crapome == "None":
	crapome = "FALSE"


if label == "false":
	label = "FALSE"
elif label == "true":
	label = "TRUE" 

cmd = r"Rscript /home/bornea/galaxy_moffitt_dev/tools/Moffitt_Tools/bubblebeam/bubbles_v9_NSAF_natural_log.R " + str(list_file) + r" " + str(prey_file) + r" " + str(crapome) + r" " + str(color) + r" " + str(label) + r" " + str(cutoff) + r" " + str(mq_sc)
os.system(cmd)
time.sleep(3)

open('./output.txt')
os.rename('output.txt', str(output_file_name))

open('./bubble_zoom_NSAF.png')
os.rename('bubble_zoom_NSAF.png', str(bub_zoom_NSAF))

open('./bubble_zoom_SAINT.png')
os.rename('bubble_zoom_SAINT.png', str(bub_zoom_SAINT))

open('./bubble_SAINT.png')
os.rename('bubble_SAINT.png', str(bub_SAINT))

open('./bubble_NSAF.png')
os.rename('bubble_NSAF.png', str(bub_NSAF))

