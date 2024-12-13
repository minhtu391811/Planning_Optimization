import sys

# Function to read input
def read_input():
    [n] = [int(x) for x in sys.stdin.readline().split()]  # Number of variables
    domains = {}  # Dictionary to store domain of each variable

    for i in range(1, n + 1):
        domains[i] = [int(j) for j in sys.stdin.readline().split()]
        
    LEQ = []
    EQ = []
    while True:
        data = [i for i in sys.stdin.readline().split()]
        if data[0] == "LEQ":
            [i, j, D] = [int(data[1]), int(data[2]), int(data[3])]
            LEQ.append([i, j, D])
        elif data[0] == "EQ":
            [i, j, a, b] = [int(data[1]), int(data[2]), int(data[3]), int(data[4])]
            EQ.append([i, j, a, b])
        elif data[0] == "#":
            break

    return n, domains, LEQ, EQ

n, domains, LEQ, EQ = read_input()  # Read the input
l1 = len(LEQ)
l = len(EQ) + l1

def AC3():
    global domains
    Q = []
    k = 0
    for [i, j, D] in LEQ:
        Q.append([i, k])
        Q.append([j, k])
        k += 1
    
    for [i, j, a, b] in EQ:
        Q.append([i, k])
        Q.append([j, k])
        k += 1
    
    while Q:
        [x, c] = Q[0]
        Q.remove([x, c])
        if revise_AC3(x, c):    
            if len(domains[x]) == 0:
                return False
            else:
                for c1 in range(l1):
                    if c1 != c:
                        [i, j, D] = LEQ[c1]
                        if x == i:
                            Q.append([j, c1])
                        if x == j:
                            Q.append([i, c1])
                for c1 in range(l1, l):
                    if c1 != c:
                        [i, j, a, b] = EQ[c1 - l1]
                        if x == i:
                            Q.append([j, c1])
                        if x == j:
                            Q.append([i, c1])
                                
    return True

def Check_AC3(c, x, v):
    global constraints
    global domains
    if c < l1:
        [i, j, D] = LEQ[c]
        if x == i:
            for v1 in domains[j]:
                if v <= v1 + D:
                    return True
        if x == j:
            for v1 in domains[i]:
                if v1 <= v + D:
                    return True
    else: 
        [i, j, a, b] = EQ[c - l1]
        if x == i:
            for v1 in domains[j]:
                if v == a*v1 + b:
                    return True
        if x == j:
            for v1 in domains[i]:
                if v1 == a*v + b:
                    return True
    return False

def revise_AC3(x, c):
    global domains
    new_domain = list(domains[x])
    CHANGE = False
    for v in domains[x]:
        if not Check_AC3(c, x, v):
            new_domain.remove(v)
            CHANGE = True
    domains[x] = new_domain
    return CHANGE



if AC3():
    for i in range(1, n + 1): 
        print(len(domains[i]), *domains[i])
else: 
    print('FAIL')