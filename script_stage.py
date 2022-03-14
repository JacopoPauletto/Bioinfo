#!/usr/bin/env python
# coding: utf-8

# In[1]:


import gzip
import sys
from Bio import SeqIO
from random import sample


# In[2]:


program = sys.argv[0]
Path_FASTA = sys.argv[1]
percent_seqs = sys.argv[2]

print("Program name : " + program)
print("Path al FASTA : " + Path_FASTA)
print("Percent of sequences : " + percent_seqs) 


# In[3]:


inFile = gzip.open(sys.argv[1], 'rt')
try:
    inFile.read(1)
    inFile = gzip.open(sys.argv[1], 'rt') 
except OSError:
    inFile = open(sys.argv[1], 'rt')


# In[4]:


headerList = []
for record in SeqIO.parse(inFile,'fasta'):
    headerList.append(record.id)


# In[5]:


random_seqs = sample(headerList,int(len(headerList)*int(percent_seqs)/(100)))
outFile = open('my_fasta.txt','w')
for seq in SeqIO.parse(inFile,'fasta') :
    if seq.id in random_seqs:
        SeqIO.write(seq, outFile, 'fasta')
    else :
        continue 
 
    
    

    

