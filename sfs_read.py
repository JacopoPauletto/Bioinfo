
import sys
import inspect

program = sys.argv[0]
path_to_sfs = sys.argv[1] 



inFile = open(sys.argv[1], 'r')
sfs_dict = dict()
t = tuple()
i = 1 
for line in inFile :
    a,b,c,d,e = line.split()
    t = (a,b,c,d,e)
    sfs_dict[i] = t
    i = i+1
inFile.close()

