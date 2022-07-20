import sys
from Bio import SeqIO 
from Bio.Seq import Seq

program = sys.argv[0]
path_to_matches = sys.argv[1]
path_to_fa = sys.argv[2]
path_to_chr = sys.argv[3]

tuple_id = ()
inFile_fa = open(sys.argv[2], "r")
for record in SeqIO.parse(inFile_fa, "fasta"):
    tuple_id = tuple_id + ((record.id, record.seq), )


SMEM_dict = {}
temp = ()
sequence = ""
seq = ""
s = ""
count = 0
inFile_matches = open(sys.argv[1], 'r')
for line in inFile_matches :
    a = (line,)
    temp = temp + a
    if line[0] == '/' :
        for element in temp :
            if element[0] == "S":
                id, read, len = element.split()
                readid, startpos, endpos = read.split("-",2)
                t = (readid,)
                if readid not in SMEM_dict :
                    SMEM_dict[readid] = []
                t = ()
                for value in tuple_id :
                    if read in value :
                        sequence = value[1]
            elif element[0] == 'E':
                count = count + 1
                smemid, start, length, hit, cromosome = element.split()
                crom, strandAndPoscrom = cromosome.split(":", 1)
                strand = strandAndPoscrom[0]
                poscrom = strandAndPoscrom.replace(strand,"")
                if strand == "-" :
                    sequence = sequence.reverse_complement()
                if count == 1 :
                    for character in range(int(start), int(length)):
                        seq = seq + sequence[character]
                    smems = (crom, poscrom, strand, startpos, int(length)-int(start), seq, "norm")
                    SMEM_dict[readid].append(smems)
                    seq = ""
                    s = ""
                else :
                    if strand == "-" :
                        sequence = sequence.reverse_complement()
                    for character in range(int(start), int(length)):
                        seq = seq + sequence[character]
                    smems = (crom, poscrom, strand, start, int(length)-int(start), seq, "exc", startpos, length)
                    SMEM_dict[readid].append(smems)
                    seq = ""
                    s = ""
            
        sequence = ""
        count = 0
        temp = ()   



arr = []
inFile_chr = open(sys.argv[3], "r")
outFile = open("outFile.sam", "w")
for line in inFile_chr :
    if line[0] == ">" :
        strand, dna, chromosome, ref = line.split()
        chr, name, strn, val1, len, val2 = chromosome.split(":", 5)
        outFile.write("%s\t%s\n"
            % ("@HD", "VN:1.4"))
        outFile.write("%s\t%s\t%s%i\n"
            % ("@SQ", "SN:"+strn, "LN:", int(len) ))
for key, values in SMEM_dict.items() :
    for elements in values :
        count = count + 1
    if count > 1:
            element = values[count-1]
            if element[6] == "exc" :
                k = key+"-"+str(element[7])+"-"+str(element[8])
                for element in values :
                   if element[2] == "+" :
                        outFile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                        % (k, "0", element[0], element[1], "255", str(element[4])+"M", "*", "0", "0", element[5], "*"))
                   else :
                       outFile.write("%s\t%s\t%s\t%i\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                        % (k, "16", element[0], int(element[1]), "255", str(element[4])+"M", "*", "0", "0", element[5], "*"))
                k = ""
            else :
                for element in values :
                    if element[2] == "+" :
                        outFile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                         % (key+"-"+str(element[3])+"-"+str(element[4]), "0", element[0], element[1], "255", str(element[4])+"M", "*", "0", "0", element[5], "*"))
                    else :
                        outFile.write("%s\t%s\t%s\t%i\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                         % (key+"-"+str(element[3])+"-"+str(element[4]), "16", element[0], int(element[1]), "255", str(element[4])+"M", "*", "0", "0", element[5], "*"))
    else :
        for element in values :
            if element[2] == "+" :
                outFile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                % (key+"-"+str(element[3])+"-"+str(element[4]), "0", element[0], element[1], "255", str(element[4])+"M", "*", "0", "0", element[5], "*"))
            else :
                outFile.write("%s\t%s\t%s\t%i\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                % (key+"-"+str(element[3])+"-"+str(element[4]), "16", element[0], int(element[1]), "255", str(element[4])+"M", "*", "0", "0", element[5], "*"))

    count = 0
 
