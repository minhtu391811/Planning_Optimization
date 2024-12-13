from ortools.linear_solver import pywraplp
import sys
import math

def input() :
    [m,n] = [int(x) for x in sys.stdin.readline().split()]
    P = []
    for i in range(m):
        r = [int(x) - 1 for x in sys.stdin.readline().split()][1:]
        P.append(r)
        
    [K] = [int(x) for x in sys.stdin.readline().split()]
    B = []
    for k in range(K):
        [i,j] = [int(x) - 1 for x in sys.stdin.readline().split()]
        B.append([i, j])
    return m, n, P, B

m, n, P, B = input()

# create solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# define decision variables
# x[i][t] = 1 means course i is assigned to teacher t
x =  [[solver.IntVar(0, 1, 'x(' + str(i) + ',' + str(t) + ')') for t in range(m)] for i in range(n)]

# y[t] is the load number of teacher t
y = [solver.IntVar(0, n, 'y(' + str(t) + ')') for t in range(m)]

#z represents the objective function
z = solver.IntVar(0, n, 'z')

# state constraints
for t in range(m):
    for i in range(n):
        if not (i in P[t]) :
            c = solver.Constraint(0, 0)
            c.SetCoefficient(x[i][t], 1)

for [i, j] in B: 
    for t in range(m):
        c = solver.Constraint(0, 1)
        c.SetCoefficient(x[i][t], 1)
        c.SetCoefficient(x[j][t], 1)
        
for t in range(m):
    c = solver.Constraint(0, 0)
    for i in range(n):
        c.SetCoefficient(x[i][t], 1)
    c.SetCoefficient(y[t], -1)
    
for i in range(n):
    c = solver.Constraint(1, 1)
    for t in range(m):
        c.SetCoefficient(x[i][t], 1)

for t in range(m):
    c = solver.Constraint(0,n)
    c.SetCoefficient(z, 1)
    c.SetCoefficient(y[t], -1)

obj = solver.Objective()
obj.SetCoefficient(z, 1)
obj.SetMinimization()

status = solver.Solve()
if status != pywraplp.Solver.OPTIMAL:
    print (-1)
else:
    print (math.floor(solver.Objective().Value()))
