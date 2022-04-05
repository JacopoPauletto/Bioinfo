import sys
import inspect

program = sys.argv[0]
path_to_sfs = sys.argv[1] 


inFile = open(sys.argv[1], 'r')
sfs_dict = dict()
for line in inFile : 
    key, value = line.split()
    sfs_dict[key]= value 
inFile.close()