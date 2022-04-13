import sys
import inspect
from Bio import SeqIO

program = sys.argv[0]       
path_to_sfs = sys.argv[1]   
path_to_fq = sys.argv[2]

inFile = open(sys.argv[1], 'r') 
sfs_dict = dict()
t = tuple()
read_name = ''
mykey = list()
#Filling dictionary with all elements from the SFS by using read's identifiers as keys
for line in inFile :
    id_read, seq, start_position, lenght, n_occurence = line.split()
    t = (seq, start_position, lenght, n_occurence)
    #Checking if a SFS row starts with a read's identifier or is part of the previous one
    if id_read != '*' :
        read_name = id_read
        sfs_dict[read_name] = []
    sfs_dict[read_name].append(t) 
inFile.close()

"""
seq = ''
with open(sys.argv[2]) as fastq_file:
   for record in SeqIO.parse(fastq_file, "fastq"):
       seq = str(record.seq)
       print(type(seq))
       for key, value in sfs_dict.items() :
         if record.id == key :
            for element in value :
                position = int(element[1])
                for character in range(position,(position+int(element[2])-1)) :
                    seq[character] = '_'
       print(seq)                  
       
"""

new_record = dict()
record_dict = SeqIO.to_dict(SeqIO.parse(sys.argv[2], "fastq"))
for key, value in record_dict.items() :
    sequence = ''
    for k, v in sfs_dict.items() :
         if key == k :
            seq = list(value)
            for element in v :
               position = int(element[1])
               for character in range(position,(position+int(element[2])-1)) :
                   seq[character] = '_'
    sequence = sequence.join(seq) 
    start = 0
    end = 0     
    #for char in sequence:
     #   if char != '_' :
      #      end = end + 1 
       # else :
        #    start = start + 1
         #   end = start 