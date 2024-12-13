import sys

# Function to read input
def read_input():
    [n] = [int(x) for x in sys.stdin.readline().split()]  # Number of variables
    domains = {}  # Dictionary to store domain of each variable

    for i in range(1, n + 1):
        domains[i] = list()
        data = sys.stdin.readline().split()
        k = int(data[0])  # Number of values in the domain of Xi
        for j in range(1, len(data)):
            domains[i].append(int(data[j]))
    
    [m] = [int(x) for x in sys.stdin.readline().split()]  # Number of constraints
    constraints = []

    for _ in range(m):
        [i, j, D] = [int(x) for x in sys.stdin.readline().split()]
        constraints.append((i, j, D))

    return n, m, domains, constraints

n, m, domains, constraints = read_input()  # Read the input

def AC3():
    global domains
    Q = []
    a = 0
    for [i, j, D] in constraints:
        Q.append([i, a])
        Q.append([j, a])
        a += 1
    while Q:
        [x, c] = Q[0]
        Q.remove([x, c])
        if revise_AC3(x, c):    
            if len(domains[x]) == 0:
                return False
            else:
                for c1 in range(m):
                    if c1 != c:
                        [i, j, D] = constraints[c1]
                        if x == i:
                            Q.append([j, c1])
                        if x == j:
                            Q.append([i, c1])
                                
    return True

def Check_AC3(c, x, v):
    global constraints
    global domains
    [i, j, D] = constraints[c]
    if x == i:
        for v1 in domains[j]:
            if v <= v1 + D:
                return True
    if x == j:
        for v1 in domains[i]:
            if v1 <= v + D:
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