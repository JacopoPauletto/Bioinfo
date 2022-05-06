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
not_found = dict()
outFile_fa = open('non_specific_read.fa', 'w')
record_dict = SeqIO.to_dict(SeqIO.parse(sys.argv[2], "fastq"))
#Replacing the specific parts of the sequence in FASTQ file with the '-' character 
for key, value in record_dict.items() :
    sequence = ''
    found = False
    for k, v in sfs_dict.items() :
         if key == k :
            found = True
            seq = list(value)
            for element in v :
               position = int(element[1])
               for character in range(position,(position+int(element[2]))) :
                   seq[character] = '_'
    if found :
        sequence = sequence.join(seq) 
        start = 0
        end = 0
        i = 0
        char_to_keep = ''
        string_to_keep = list()
        dict_value = tuple()
        #Creating a new dictionary with the non-specific sequences and their position on the read
        for i in range(0,len(sequence)-1) :
            if sequence[i] != '_' :
                if len(char_to_keep) == 0 :
                    start = i
                char_to_keep = char_to_keep+(sequence[i])
            else :
                if len(char_to_keep) != 0 :
                    end = i
                    dict_value = (char_to_keep,start,end)
                    new_record.setdefault(key, []).append(dict_value)
                    char_to_keep = ''
        if len(char_to_keep) != 0:
            end = len(sequence)-1
            dict_value = (char_to_keep,start,end)
            new_record.setdefault(key, []).append(dict_value)
            char_to_keep = ''
    else :
        not_found.setdefault(key, [])


#Writing a FASTA file with non-specific read to reiterate on them and looking for new specifics 
for k, v in new_record.items() :
    for single in v:
        outFile_fa.write(">%s-%i-%i \n"
        % (k, single[1], single[2]))
        outFile_fa.write("%s \n" % (single[0]))

#Changing form FASTA to FASTQ with dummys quality 
outFile_fq = open("non_specific_read.fq", "w")
for r in SeqIO.parse("non_specific_read.fa", "fasta"):
    r.letter_annotations["phred_quality"] = [40] * len(r)
    SeqIO.write(r, outFile_fq, "fastq")
    

