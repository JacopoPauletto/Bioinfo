#!/usr/bin/env python
# coding: utf-8



import gzip
import sys
from Bio import SeqIO
from random import sample





program = sys.argv[0]
Path_FASTA = sys.argv[1]
percent_seqs = sys.argv[2]

print("Program name : " + program)
print("Path al FASTA : " + Path_FASTA)
print("Percent of sequences : " + percent_seqs) 




inFile = gzip.open(sys.argv[1], 'rt')
try:
    inFile.read(1)
    inFile = gzip.open(sys.argv[1], 'rt') 
except OSError:
    inFile = open(sys.argv[1], 'rt')



headerList = []
for record in SeqIO.parse(inFile,'fasta'):
    headerList.append(record.id)
inFile.seek(0)




"""
inFile = gzip.open(sys.argv[1], 'rt')
try:
    inFile.read(1)
    inFile = gzip.open(sys.argv[1], 'rt') 
except OSError:
    inFile = open(sys.argv[1], 'rt')
"""


# In[6]:


random_seqs = sample(headerList,int(len(headerList)*float(percent_seqs)/(100)))
outFile = open('my_fasta.fa','w')
for record in SeqIO.parse(inFile,'fasta') :
    if record.id in random_seqs:
        SeqIO.write(record, outFile, 'fasta')
    else :
        continue 
 
    
    

    

