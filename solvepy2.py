import sys

answer = [] # Assignment A 
l = 1

def clause_strip(clause):
    #used in parsing the DIMACS format input
    ret = []
    tmp = []
    for i in clause:
        if (i == '0'):
            ret.append(tmp)
            tmp = []
        elif (i == '%'):
            break
        else: 
            tmp.append(int(i))
    return ret

def containsUnit(clauses, num):
    for i in range(len(clauses)):
        if (len(clauses[i]) == num):
            return i
    return -1

def deduction(clauses, v):
    i = 0
    nv = -1*v
    while (i < len(clauses)):
        if v in clauses[i]:
            del clauses[i]
            continue
        elif nv in clauses[i]:
            clauses[i].remove(nv)
        i += 1
    return clauses

def DPLL(clauses):
    global answer
    global l

    i = containsUnit(clauses, 1)
    while (i>=0):
        #deduction process
        v = clauses[i][0]
        answer.append(v)
        del clauses[i]
        clauses = deduction(clauses, v)
        i = containsUnit(clauses, 1)

    if (containsUnit(clauses, 0) > 0):
        #solve conflict
        return False
    
    if (len(clauses) == 0):
        return True

    while (l < nVar):
        if (l not in answer) and (-1*l not in answer): 
            break 
        l += 1
    
    if DPLL(clauses+[[l]]):
        return True
    elif DPLL(clauses+[[-1*l]]): 
        return True
    else:
        return False
    

file_name = sys.argv[1]
clauses = []
comments = [] #line starts with 'c' in .cnf file
nVar = 0
nClause = 0

f = open(file_name,'r')
line = f.readline()
#read the answer in DIMACS format.
while line:
    if (line[0] == 'c'):
        x = line[1:].strip()
        if x:
            comments.append(x)
    elif (line[0] == 'p'):
        x = line.strip().split()
        nVar = int(x[2])
        nClause = int(x[3])
        lines = f.read()
        clauses = lines.strip().split()
        break 

    line = f.readline()

clauses = clause_strip(clauses)
ans = DPLL(clauses)

#print the answer in DIMACS Format
if (ans):
    print("s SATISFIABLE")
    answer.append(0)
    print("v "+ " ".join(map(str,answer)))
else:
    print("s UNSATISFIABLE")
f.close()

