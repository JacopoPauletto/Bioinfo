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


new_record = dict()
outFile_fa = open('non_specific_read.fa', 'w')
record_dict = SeqIO.to_dict(SeqIO.parse(sys.argv[2], "fastq"))
for key, value in record_dict.items() :
    sequence = ''
    for k, v in sfs_dict.items() :
         if key == k :
            seq = list(value)
            for element in v :
               position = int(element[1])
               for character in range(position,(position+int(element[2]))) :
                   seq[character] = '_'
    sequence = sequence.join(seq) 
    start = 0
    end = 0
    i = 0
    char_to_keep = ''
    string_to_keep = list()
    dict_valeu = tuple()
    for i in range(0,len(sequence)-1) :
        if sequence[i] != '_' :
            if len(char_to_keep) == 0 :
                start = i
            char_to_keep = char_to_keep+(sequence[i])
        else :
            if len(char_to_keep) != 0 :
                #string_to_keep.append(char_to_keep)
                end = i
                dict_value = (char_to_keep,start,end)
                new_record.setdefault(key, []).append(dict_value)
                char_to_keep = ''
    #v = (''.join(''.join(val)) for val in new_record[key])
    #outFile.write(">" + key + " | " + v)
        
    #SeqIO.write(new_record, outFile, 'fasta')

for k, v in new_record.items() :
    for single in v:
        outFile_fa.write(">%s-%i-%i \n"
        % (k, single[1], single[2]))
        outFile_fa.write("%s \n" % (single[0]))

outFile_fq = open("non_specific_read.fq", "w")
for r in SeqIO.parse("non_specific_read.fa", "fasta"):
    r.letter_annotations["phred_quality"] = [40] * len(r)
    SeqIO.write(r, outFile_fq, "fastq")
    

