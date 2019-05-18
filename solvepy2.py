import sys

answer = []
#have to solve right variable answer. 
#depth issue. 

def clause_strip(clause):
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
    print(clauses)
    i = containsUnit(clauses, 1)
    global answer
    while (i>0):
        #deduction process
        v = clauses[i][0]
        answer.append(i)
        del clauses[i]
        clauses = deduction(clauses, v)
        i = containsUnit(clauses, 1)
    
    if (containsUnit(clauses, 0) > 0):
        return False
    if (len(clauses) == 0):
        return True 

    l = 1
    while (l in answer):
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
cnfFormat = ''

f = open(file_name,'r')
line = f.readline()
while line:
    if (line[0] == 'c'):
        x = line[1:].strip()
        if x:
            comments.append(x)
    elif (line[0] == 'p'):
        x = line.strip().split()
        cnfFormat = x[1]
        nVar = int(x[2])
        nClause = int(x[3])
        lines = f.read()
        clauses = lines.strip().split()
        break 

    line = f.readline()

clauses = clause_strip(clauses)
ans = DPLL(clauses)
print(answer)
f.close()

