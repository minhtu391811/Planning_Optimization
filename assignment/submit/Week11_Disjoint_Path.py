from ortools.sat.python import cp_model
import sys

def input():
    [n, m] = [int(x) for x in sys.stdin.readline().split()]
    C = []
    A = {}
    B = {}
    for i in range(1,n+1):
        A[i] = []
        B[i] = []
    for _ in range(m):
        [u, v, c] = [int(x) for x in sys.stdin.readline().split()]
        A[u].append(v)
        B[v].append(u)
        C.append([u,v,c])
        # C.append([v,u,c])
    
    return n, m, A, B, C

n, m, A, B, C = input()

model = cp_model.CpModel()
x1 = {}
x2 = {}
for [i,j,c] in C:
    x1[i, j] = model.NewIntVar(0, 1, 'x1[' + str(i) + ',' + str(j) + ']')
    x2[i, j] = model.NewIntVar(0, 1, 'x2[' + str(i) + ',' + str(j) + ']')
obj = model.NewIntVar(0, 20000, 'obj')

for [i,j,c] in C:
    model.Add(x1[i,j] + x2[i,j] <= 1)

for i in range(1, n + 1):
    model.Add(sum(x1[u,i] for u in B[i]) - sum(x1[i,v] for v in A[i]) == (-1 if i == 1 else 1 if i == n else 0))
    model.Add(sum(x2[u,i] for u in B[i]) - sum(x2[i,v] for v in A[i]) == (-1 if i == 1 else 1 if i == n else 0))

model.Add(obj == sum(c*(x1[u,v] + x2[u,v]) for [u,v,c] in C))
model.Minimize(obj)

solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 10.0
solver.parameters.num_search_workers = 1  # Giảm số lượng luồng xuống 1
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(solver.Value(obj))
else:
    print('NOT_FEASIBLE')