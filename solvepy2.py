import sys
import copy
import random

assigned = []
learned = []

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

def containsUnit(clauses, num, answer):
    for i in range(len(clauses)):
        count = 0
        for j in clauses[i]:
            if j in answer:
                break
            if -1*j not in answer:
                count += 1
        if count == num:
            return i
    return -1

def isClauseEmpty(clauses, answer):
    if len(clauses)== 0:
        return True
    for i in clauses:
        for j in i:
            if j in answer:
                break
            if -1*j not in answer:
                return False
    return True
    

def unitPropa(clauses, v):
    i = 0
    while (i < len(clauses)):
        if v in clauses[i]:
            clauses.pop(i)
            continue
        i += 1
    return clauses

def resolution(a1, a2):
    for i in a1:
        if -1*i in a2:
            a1.remove(i)
            a2.remove(-1*i)
            a1.extend(a2)
            a1 = list(set(a1))
            return a1
    return a1.extend(a2)

def conflict(graph_e, c_clause):
    global assigned
    global learned

    tmp = []
    #backtracking
    for i in tmp:
        if -1*i not in assigned:
            continue
        j = len(assigned)-1
        while (j >= 0):
            x = assigned.pop()
            if x == -1*i: 
                break

    #add the learned clause
    if len(tmp) != 0:
        learned.append(tmp)

def DPLL(clauses, answer, graph_e):
    global assigned
    global learned

    clauses.extend(learned)

    i = containsUnit(clauses, 1, answer)
    #print(clauses)
    while (i>=0):
        #Unit propagation
        v = clauses[i][0]
        for j in clauses[i]:
            if -1*j not in answer and j not in answer:
                v = j
                break
        answer.append(v)

        for j in clauses[i]:
            if j != v:
                graph_e.append((-1*j, v))
    
        clauses.pop(i)
        clauses = unitPropa(clauses, v)
        i = containsUnit(clauses, 1, answer)

    if (isClauseEmpty(clauses, answer)):
        return answer
    
    c_index = containsUnit(clauses, 0, answer)
    if (c_index >= 0):
        print("conflict")
        conflict(graph_e, clauses[c_index])
        return False
   
    backup1 = copy.deepcopy(clauses)
    backup2 = copy.deepcopy(clauses)
    ans1 = copy.deepcopy(answer)
    ans2 = copy.deepcopy(answer)
    e1 = copy.deepcopy(graph_e)
    
    l = random.randrange(1, nVar)
    while (l in answer) or (-1*l in answer):
        l = random.randrange(1, nVar)

    assigned.append(l)
    v = DPLL(backup1 + [[l]], ans1, e1)
    if v:
        return v
    
    if l in assigned:
        assigned.remove(l)
        assigned.append(-1*l)
    else:
        return False

    e2 = copy.deepcopy(graph_e)

    v = DPLL(backup2 + [[-1*l]], ans2, e2)
    if v: 
        return v
    
    if -1*l in assigned:
        assigned.remove(-1*l)

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
f.close()

clauses = clause_strip(clauses)
ans = DPLL(clauses, [], [])

#print the answer in DIMACS Format
if (ans):
    print("s SATISFIABLE")
    ans.append(0)
    print("v "+ " ".join(map(str,ans)))
else:
    print("s UNSATISFIABLE")