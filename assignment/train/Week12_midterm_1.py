import sys

IE_constraints = []
LTE_contraints = []
AD_constraints = 0

[n] = [int(i) for i in sys.stdin.readline().split()]
x = [0 for i in range(n + 1)]
data = [int(i) for i in sys.stdin.readline().split()]
for i in range(1, n + 1):
    x[i] = data[i - 1]

# Tinh violations AllDifferent
def AD_violations():
    AD_vio = 0
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            if x[i] == x[j]:
                AD_vio += 1
    return AD_vio

# Tinh violations IsEqual
def IE_violations(i,j):
    return abs(x[int(i)] - x[int(j)])

# Tinh violations LessThanEqual
def LTE_violations(i, j):
    return max(0, int(x[int(i)] - x[int(j)]))
    
def Violations():
    global violations
    violations = 0
    for [i,j] in IE_constraints:
        v = IE_violations(i, j)
        violations += v
    for [i,j] in LTE_contraints:
        v = LTE_violations(i,j)
        violations += v
    if AD_constraints == 1:
        v = AD_violations()
        violations += v
    return violations
    
while True:
    data = [x for x in sys.stdin.readline().split()]
    if data[0] == 'post':
        if data[1] == 'IsEqual':
            [i,j] = [data[2], data[3]]
            IE_constraints.append([i,j])
        if data[1] == 'LessThanEqual':
            [i,j] = [data[2], data[3]]
            LTE_contraints.append([i,j])
        if data[1] == 'AllDifferent':
            AD_constraints = 1
    elif data[0] == 'violations':
        print(Violations())
    elif data[0] == 'update':
        [i,v] = [data[1], data[2]]
        x[int(i)] = int(v)
    elif data[0] == '#':
        break    
        