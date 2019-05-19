import sys
import copy
import random

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

def unitPropa(clauses, v):
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

def DPLL(clauses, answer):
    #print("THIS IS C")
    #print(clauses)

    i = containsUnit(clauses, 1)
    while (i>=0):
        #Unit propagation
        v = clauses[i][0]
        answer.append(v)
        del clauses[i]
        clauses = unitPropa(clauses, v)
        i = containsUnit(clauses, 1)

    #print("THIS IS A")
    #print(answer)

    if (len(clauses) == 0):
        return answer
    
    if (containsUnit(clauses, 0) >= 0):
        #learned clause 
        #print("CONFLICT CASE")
        return False
   
    backup1 = copy.deepcopy(clauses)
    backup2 = copy.deepcopy(clauses)
    ans1 = copy.deepcopy(answer)
    ans2 = copy.deepcopy(answer)

    l = random.randrange(1, nVar)
    while (l in answer) or (-1*l in answer):
        l = random.randrange(1, nVar)

    v = DPLL(backup1 + [[l]], ans1)

    if v:
        print("INSIDE ")
        return v
    v = DPLL(backup2 + [[-1*l]], ans2)
    if v: 
        return v
    
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
ans = DPLL(clauses, [])

#print the answer in DIMACS Format
if (ans):
    print("s SATISFIABLE")
    ans.append(0)
    print("v "+ " ".join(map(str,ans)))
else:
    print("s UNSATISFIABLE")
f.close()

