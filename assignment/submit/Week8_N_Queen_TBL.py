import random as rd

n = int(input())
x = [0 for i in range(n)]
T = [[0 for i in range(n)] for i in range(n)]
tbl = 10
violation = 0

# return the violation 
def get_violation():
    v = 0 
    for i in range(n):
        for j in range(i + 1, n):
            if x[i] == x[j] or abs(x[i] - x[j]) == abs(i - j):
                v += 1
    return v

# generate random initial solution x[]
def generate_initial_solution():
    global violation
    
    for i in range(n):
        x[i] = rd.randint(0, 9)
    violation = get_violation()
    
# return the violation change if queen q is moved to row r
def get_delta(q, r):
    oldV = x[q]
    x[q] = r # move queen q to row r
    newV = get_violation()
    delta = newV - violation
    x[q] = oldV # undo the move
    return delta 

# select the move in iteration it
def select_tabu(it):
    global violation
    minD = 1e9
    L = []
    
    for q in range(n):
        for r in range(n):
            if x[q] != r:
                if T[q][r] <= it:
                    delta = get_delta(q, r)
                    if delta < minD:
                        minD = delta
                        L = [[q, r]]
                    elif delta == minD:
                        L.append([q, r])
    
    i = rd.randint(0, len(L) - 1)
    return L[i], minD

def search_tabu(max_iter):
    global violation
    
    generate_initial_solution()
    print('Initial violations = ',violation)

    for it in range(max_iter):
        if violation == 0:
            break
        
        [q, r], delta = select_tabu(it)
        x[q] = r
        T[q][r] = it + tbl
        violation = get_violation()
        print('Step ',it,': Move (',q,',',r,'), delta = ',delta,' new violations = ',violation)
        
    print(n)
    for i in x:
        print(i + 1, end = " ")

search_tabu(10000)