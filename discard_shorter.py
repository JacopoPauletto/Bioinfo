import sys
from Bio import SeqIO 

program = sys.argv[0]                       
path_to_fa = sys.argv[1]   
len_to_discard= sys.argv[2]

#discard all the reads with a non-specifc shorter than a "n" value 
inFile = open(sys.argv[1], 'r') 
outFile = open("disc_non_specific.fa", 'w')
for record in SeqIO.parse(inFile, "fasta"):
    if len(record.seq) >= int(sys.argv[2]) :
        SeqIO.write(record, outFile, "fasta")
