import sys

program = sys.argv[0]                       
path_to_sfs = sys.argv[1] 


sfs_dict = dict()
t = tuple()
read_name = ''
mykey = list()
inFile = open(sys.argv[1], "r")
for line in inFile :
    id_read, seq, start_position, lenght, n_occurence = line.split()
    t = (seq, start_position, lenght, n_occurence)
    if id_read != '*' :
        read_name = id_read
        sfs_dict[read_name] = []
    sfs_dict[read_name].append(t) 

list = []
count = 0
char_to_keep = ""
new_sfs_dict = dict()
for key, value in sfs_dict.items() :
    new_sfs_dict[key] = []
    for element in value :
        list.append(element) 
        count = count + 1 
    start = count
    first = list[start-1]
    last = list[0]
    for el in list :
        el1 = list[count-1]
        el2 = list[count-2]
        if  (start > 1):
            if count == 1:
                new_sfs_dict[key].append(a) 
            if (int(el1[1])+int(el1[2])) >= int(el2[1]) :
                n_char_to_keep = (int(el2[1])-int(el1[1])) + (int(el2[2])-int(el1[2]))  
                sequence = el2[0]
                start_seq = first[0]
                pos = first[1]
                for index in range((len(sequence)-n_char_to_keep), len(sequence)) :
                    char_to_keep = char_to_keep + sequence[index]
                start_seq = start_seq + char_to_keep
                a = (start_seq, pos, len(start_seq), first[3])
            else :
                if el1 == first :
                    b = el1
                    new_sfs_dict[key].append(b)
                    first = el2
                    char_to_keep = ""
                elif el2 == last :
                    e = el2 
                    new_sfs_dict[key].append(e)
                    char_to_keep = ""
                else :
                    new_sfs_dict[key].append(a)
                    first = el2
                    a = ()
                    char_to_keep = ""
        elif  (start == 1) :
            c = el1
            new_sfs_dict[key].append(c)
        count = count - 1 
        
    
    count = 0
    list = []
    char_to_keep = ""

"""

outSFS = open('outSFS.txt', 'w')
for key, value in new_sfs_dict.items() :
    outSFS.write(">%s-%s \n"
        % (key, value))

"""

new_sfs_out = open("new_solution_out.sfs", "w")
for key, value in new_sfs_dict.items():
    for element in value :
        if element == value[0] :
            new_sfs_out.write("%s\t%s\t%s\t%s\t%s \n"
            % (key, element[0], element[1], element[2], element[3]))
        else :
            new_sfs_out.write("%s\t%s\t%s\t%s\t%s \n"
            % ("*", element[0], element[1], element[2], element[3]))
        
