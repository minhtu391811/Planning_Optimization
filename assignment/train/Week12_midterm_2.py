import sys

# Function to read input
def read_input():
    domains = {}  # Dictionary to store domain of each variable

    for i in range(1, 4):
        domains[i] = list()
        data = sys.stdin.readline().split()
        for j in range(len(data)):
            domains[i].append(int(data[j]))

    return domains

domains = read_input()  # Read the input

def AC3():
    global domains
    Q = [1, 2, 3]
    while Q:
        x = Q[0]
        Q.remove(x)
        if revise_AC3(x):    
            if len(domains[x]) == 0:
                return False
                                
    return True

def Check_AC3(x, v):
    global constraints
    global domains
    if x == 1:
        for v2 in domains[2]:
            for v3 in domains[3]:
                if v + v2 <= v3:
                    return True
    if x == 2:
        for v1 in domains[1]:
            for v3 in domains[3]:
                if v1 + v <= v3:
                    return True
    if x == 3:
        for v1 in domains[1]:
            for v2 in domains[2]:
                if v1 + v2 <= v:
                    return True
    return False

def revise_AC3(x):
    global domains
    new_domain = list(domains[x])
    CHANGE = False
    for v in domains[x]:
        if not Check_AC3(x, v):
            new_domain.remove(v)
            CHANGE = True
    domains[x] = new_domain
    return CHANGE
    
if AC3():
    for i in range(1, 4): 
        print(*sorted(domains[i]))
else: 
    print('FAIL')