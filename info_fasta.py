import sys
import inspect
from Bio import SeqIO
from matplotlib import pyplot as plt
import numpy as np

program_name= sys.argv[0]                       
path_to_fa = sys.argv[1]

print("Name of Python script:", sys.argv[0])
print("FASTA file:", sys.argv[1])

average_len = 0
entry_counter = 0
sum = 0
max_len = 0
min_len = sys.maxsize
array_of_len = []

inFile = open(sys.argv[1], "r") 
for record in SeqIO.parse(inFile, "fasta"):
   entry_counter = entry_counter + 1
   sum = sum  + len(record.seq)
   array_of_len.append(len(record.seq))
   if len(record.seq) >= max_len :
        max_len = len(record.seq)
   if len(record.seq) <= min_len : 
        min_len = len(record.seq)


print("Number of entry:", entry_counter)
print("Maximum length:", max_len)
print("Minimum length:", min_len)
print("Average length:", sum/entry_counter)



plt.xlabel("sequence length")
plt.ylabel("number of sequences")
plt.hist(array_of_len, bins = entry_counter)
plt.show()