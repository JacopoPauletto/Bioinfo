import sys
import inspect

program = sys.argv[0]   #Passing program's name from command line (ex: <python sfs_read.py /path/...> sfs_read.py will be the name)
path_to_sfs = sys.argv[1]   #Passing path to SFS file from command line (ex: <python sfs_read.py /path/to/file.sfs>)   


inFile = open(sys.argv[1], 'r') #Open in read mode the input SFS file
sfs_dict = dict()
t = tuple()
read_name = ''

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
