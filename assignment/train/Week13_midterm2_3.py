import sys
from collections import defaultdict

def read_input():
    var = []
    domain = defaultdict(list)
    EQ = []
    LEQ = []
    NEQ = []
    while True:
        data = [i for i in sys.stdin.readline().split()]
        if data[0] == "Var":
            var.append(data[1])
            domain[data[1]] = [i for i in range(int(data[2]), int(data[3]) + 1)]
        elif data[0] == "Eq":
            data[1] = int(data[1])
            data[3] = int(data[3])
            data[5] = int(data[5])
            EQ.append(data[1:])
        elif data[0] == "Leq":
            data[1] = int(data[1])
            data[3] = int(data[3])
            data[5] = int(data[5])
            LEQ.append(data[1:])
        elif data[0] == "Neq":
            data[1] = int(data[1])
            data[3] = int(data[3])
            data[5] = int(data[5])
            NEQ.append(data[1:])
        elif data[0] == "#":
            break
        
    return var, domain, EQ, LEQ, NEQ

var, domain, EQ, LEQ, NEQ = read_input()
l1 = len(EQ)
l2 = len(LEQ) + l1
l = len(NEQ) + l2

def AC3():
    global domain
    Q = []
    k = 0
    for [a,X,b,Y,c] in EQ:
        Q.append([X, k])
        Q.append([Y, k])
        k += 1
    
    for [a,X,b,Y,c] in LEQ:
        Q.append([X, k])
        Q.append([Y, k])
        k += 1
    
    for [a,X,b,Y,c] in NEQ:
        Q.append([X, k])
        Q.append([Y, k])
        k += 1
    
    while Q:
        [x, c] = Q[0]
        Q.remove([x, c])
        if revise_AC3(x, c):    
            if len(domain[x]) == 0:
                return False
            else:
                for c1 in range(l1):
                    if c1 != c:
                        [a, X, b, Y, c] = EQ[c1]
                        if x == X:
                            Q.append([Y, c1])
                        if x == Y:
                            Q.append([X, c1])
                for c1 in range(l1, l2):
                    if c1 != c:
                        [a, X, b, Y, c] = LEQ[c1 - l1]
                        if x == X:
                            Q.append([Y, c1])
                        if x == Y:
                            Q.append([X, c1])
                for c1 in range(l2, l):
                    if c1 != c:
                        [a, X, b, Y, c] = NEQ[c1 - l2]
                        if x == X:
                            Q.append([Y, c1])
                        if x == Y:
                            Q.append([X, c1])
                                
    return True

def Check_AC3(c, x, v):
    global domain
    if c < l1:
        [a,X,b,Y,c] = EQ[c]
        if x == X:
            for v1 in domain[X]:
                if a*v == b*v1 + c:
                    return True
        if x == Y:
            for v1 in domain[Y]:
                if a*v1 == b*v + c:
                    return True
    elif c < l2: 
        [a,X,b,Y,c] = LEQ[c - l1]
        if x == X:
            for v1 in domain[X]:
                if a*v <= b*v1 + c:
                    return True
        if x == Y:
            for v1 in domain[Y]:
                if a*v1 <= b*v + c:
                    return True
    else:
        [a,X,b,Y,c] = NEQ[c - l2]
        if x == X:
            for v1 in domain[X]:
                if a*v != b*v1 + c:
                    return True
        if x == Y:
            for v1 in domain[Y]:
                if a*v1 != b*v + c:
                    return True
        
    return False

def revise_AC3(x, c):
    global domain
    new_domain = list(domain[x])
    CHANGE = False
    for v in domain[x]:
        if not Check_AC3(c, x, v):
            new_domain.remove(v)
            CHANGE = True
    domain[x] = new_domain
    return CHANGE

if AC3():
    for i in var: 
        print(len(domain[i]), *domain[i])
else: 
    print('FAIL')
    
    
    
            
            