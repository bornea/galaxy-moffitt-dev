################################################################################
"""This program will read in a SAINT 'list.txt' file and the interactions from
the consensus path db database and return all the interactions that we saw in
our experiment in a format suitable for cytoscape. This allows us to filter
before getting PPIs so that it doesn't affect our SAINT score or include
interactions that don't score well"""

"""This version was modified to work in the Moffitt Proteomics Pipeline."""
################################################################################

import itertools
import sys
import os

with open(sys.argv[1],'r') as x:
    data = []
    for line in x:
        temp = line.split()
        data.append(temp) #read in data lines

accessions = []
for i in data[1:]:
    accessions.append(i[1]) #build accession list
with open('/home/bornea/galaxy_moffitt_dev/tools/Moffitt_Tools/ConsensusPathDB_human_PPI.txt', 'rt') as y:
    db  = []
    for line in y:
        temp = line.split('\t')
        db.append(temp) #build database
GO=[]
for i in db[2:]:
    GO.append(i[2]) #all interactions
GO2 = []
for i in GO:
    GO2.append(i.split(',')) #make interactions list friendly

unfiltered_network = {}
for i in accessions:
    interactions = []
    for j in GO2:
        if i in j: #find the interactions
            if j not in interactions:#dont add duplicate interactions
                interactions.append(j)
    merged = list(itertools.chain(*interactions)) # flatten list of lists
    unfiltered_network[i]=merged #assign all possible interactions to protein in a dictionary

################################################################################
"""Still need to filter merged on PPIs from our experiment.
Should I also include the interaction confidence as a parameter?
How would I do that?"""
################################################################################

dd_network = {} #data dependent network
for i in unfiltered_network:
    temp = []
    for j in unfiltered_network[i]:
        if j in accessions:
            if j not in temp:
                if j != i:
                    temp.append(j)
    dd_network[i]=temp

################################################################################
"""Now put everything back together into SAINT format and reformat for cytoscape"""
################################################################################
with open('cytoscape.txt','wt')as y:
    header = '\t'.join(data[0])
    y.write(header + '\n')
    for i in data[1:]:
        if dd_network[i[1]] != []:
            lst = []
            x='\t'.join(i)
            for j in dd_network[i[1]]:
                lst.append(j)
            for j in lst:
                y.write(x+'\t' + j+'\n')
"""with open('list & interactions.txt','wt')as y:
    header = '\t'.join(data[0])
    y.write(header + '\n')
    for i in data[1:]:
        if dd_network[i[1]] != []:
            i.append(','.join(dd_network[i[1]]))
        x = '\t'.join(i)
        y.write(x + '\n')"""

os.rename('cytoscape.txt', sys.argv[2])
