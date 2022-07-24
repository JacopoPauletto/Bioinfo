import sys
from Bio import SeqIO 
from Bio.Seq import Seq

program = sys.argv[0]
path_to_matches = sys.argv[1]
path_to_fa = sys.argv[2]
path_to_chr = sys.argv[3]

comp_tab = str.maketrans("ACGTN", "TGCAN")

#recover the non-specifc sequences from FASTA by creating a dict witch the respective read id  
tuple_id = ()
inFile_fa = open(sys.argv[2], "r")
for record in SeqIO.parse(inFile_fa, "fasta"):
    tuple_id = tuple_id + ((record.id, record.seq), )

#create a dictionary witch read id as key and his macthes as values 
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
            #check if the line of matches file is the read id and adding it in the dictionary 
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
            #read the line of matches file relative to a match 
            elif element[0] == 'E':
                count = count + 1
                smemid, start, length, hit, cromosome = element.split()
                crom, strandAndPoscrom = cromosome.split(":", 1)
                strand = strandAndPoscrom[0]
                poscrom = strandAndPoscrom.replace(strand,"")
                #normal case = read witch only one match or two match on different sequences
                if count == 1 :
                    for character in range(int(start), int(length)):
                        seq = seq + sequence[character]
                    if strand == "-" :
                        seq = seq.translate(comp_tab)[::-1]
                    smems = (crom, poscrom, strand, startpos, int(length)-int(start), seq, "norm")
                    SMEM_dict[readid].append(smems)
                    seq = ""
                    s = ""
                #exception case = read with two or more macthes on the same sequence
                else :
                    for character in range(int(start), int(length)):
                        seq = seq + sequence[character]
                    if strand == "-" :
                       seq = seq.translate(comp_tab)[::-1]
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
#write the letterhead of the SAM file
for line in inFile_chr :
    if line[0] == ">" :
        strand, dna, chromosome, ref = line.split()
        chr, name, strn, val1, len, val2 = chromosome.split(":", 5)
        outFile.write("%s\t%s\n"
            % ("@HD", "VN:1.4"))
        outFile.write("%s\t%s\t%s%i\n"
            % ("@SQ", "SN:"+strn, "LN:", int(len) ))
#write the SAM file by taking elements fromt he dictionary
for key, values in SMEM_dict.items() :
    for elements in values :
        count = count + 1
    #checking how many matches for a read  
    if count > 1:
            element = values[count-1]
            #exception case
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
            #normale case with 2 matches
            else :
                for element in values :
                    if element[2] == "+" :
                        outFile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                         % (key+"-"+str(element[3])+"-"+str(element[4]), "0", element[0], element[1], "255", str(element[4])+"M", "*", "0", "0", element[5], "*"))
                    else :
                        outFile.write("%s\t%s\t%s\t%i\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                        % (key+"-"+str(element[3])+"-"+str(element[4]), "16", element[0], int(element[1]), "255", str(element[4])+"M", "*", "0", "0", element[5], "*"))
    #normal case 
    else :
        for element in values :
            if element[2] == "+" :
                outFile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                % (key+"-"+str(element[3])+"-"+str(element[4]), "0", element[0], element[1], "255", str(element[4])+"M", "*", "0", "0", element[5], "*"))
            else :
                outFile.write("%s\t%s\t%s\t%i\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                % (key+"-"+str(element[3])+"-"+str(element[4]), "16", element[0], int(element[1]), "255", str(element[4])+"M", "*", "0", "0", element[5], "*"))

    count = 0
 
