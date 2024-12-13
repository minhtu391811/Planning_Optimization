from ortools.linear_solver import pywraplp
import sys

def read_input():
    [n, m] = [int(i) for i in sys.stdin.readline().split()]
    A = [0 for i in range(n + 1)]
    data1 = [int(i) for i in sys.stdin.readline().split()]
    for it in range(1, n + 1):
        A[it] = data1[it - 1]
    B = [0 for i in range(m + 1)]
    data2 = [int(i) for i in sys.stdin.readline().split()]
    for it in range(1, m + 1):
        B[it] = data2[it - 1]
    C = {}
    for it in range(1, n + 1):
        C[it] = [0 for i in range(m + 1)] 
        data = [int(i) for i in sys.stdin.readline().split()]
        for j in range(1, m + 1):
            C[it][j] = data[j - 1]
    return n, m, A, B, C

n, m, A, B, C = read_input()

solver = pywraplp.Solver.CreateSolver('GLOP')
x = {}
for i in range(1, n + 1):
    for j in range(1, m + 1):
        x[i,j] = solver.NumVar(0, A[i], 'x[' + str(i) + ',' + str(j) + ']')

z = solver.NumVar(0, 1000000, 'z[' + str(i) + ']')

for i in range(1, n + 1):
    c = solver.Constraint(0, A[i])
    for j in range(1, m + 1):
        c.SetCoefficient(x[i,j], 1)
    
for j in range(1, m + 1):
    c = solver.Constraint(B[j], 1000000)
    for i in range(1, n + 1):
        c.SetCoefficient(x[i,j], 1)

c = solver.Constraint(0,0)
c.SetCoefficient(z, -1)
for i in range(1, n + 1):
    for j in range(1, m + 1):
        c.SetCoefficient(x[i,j], C[i][j])
        
obj = solver.Objective()
obj.SetCoefficient(z, 1)
obj.SetMinimization()

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
    print(m * n)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            print(i, " ", j, " ", x[i,j].solution_value())