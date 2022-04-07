import sys
import inspect

program = sys.argv[0]
path_to_sfs = sys.argv[1] 


inFile = open(sys.argv[1], 'r')
sfs_dict = dict()
t = tuple()
str = ''
for line in inFile :
    a,b,c,d,e = line.split()
    t = (b,c,d,e)
    if a != '*' :
        str = a
        sfs_dict[str] = []
    sfs_dict[str].append(t) 
inFile.close()
