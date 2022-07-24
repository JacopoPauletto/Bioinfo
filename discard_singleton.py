import sys
import inspect
from Bio import SeqIO
from collections import Counter

program = sys.argv[0]                       
path_to_non_specific_fa = sys.argv[1]
value = 0
new_list = []
read_list = []

#create a list from the non-specifics FASTA containing only the read id without start and end position
inFile = open(sys.argv[1], 'r')
for record in SeqIO.parse(inFile, "fasta"):
    read_id, start, end = record.id.split("-", 2)
    read_list = read_list + [read_id] 
inFile.close()

#create a new list from the previous one with only the reads that had two or more non-specifics
for element in read_list :
    value = read_list.count(element)
    if value >= 2:
        new_list = new_list + [element]
    value = 0

#write the new FASTA containing only the reads checked before 
inFile = open(sys.argv[1], 'r')
outFile = open("disc_singleton_non_spec.fa", "w")
for r in SeqIO.parse(inFile, "fasta"):
    read_id, start, end = r.id.split("-", 2)
    if read_id in new_list:
        SeqIO.write(r, outFile, "fasta")

