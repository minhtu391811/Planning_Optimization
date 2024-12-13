from ortools.sat.python import cp_model
import sys

# Đọc dữ liệu đầu vào
def input():
    [n, m, s, L] = [int(x) for x in sys.stdin.readline().split()]
    A = {}
    T = [[0 for i in range(1, 21)] for j in range(1, 21)]
    C = [[0 for i in range(1, 21)] for j in range(1, 21)]

    for i in range(1, n + 1):
        A[i] = []
        
    for i in range(m):
        [u, v, t, c] = [int(x) for x in sys.stdin.readline().split()]
        A[u].append(v)
        A[v].append(u)
        T[u][v] = T[v][u] = t
        C[u][v] = C[v][u] = c 
    
    return n, m, s, L, A, T, C

n, m, s, L, A, T, C = input()
# for i in range(1, n + 1):
#     print(A[i])

E = []
for i in range(1, n + 1):
    for j in A[i]:
        E.append([i, j])

model = cp_model.CpModel()
x = {}
y = {}
z = {}
for i in range(1, n + 1):
    x[i] = model.NewIntVar(1, n, 'x[' + str(i) + ']')
    y[i] = model.NewIntVar(0, 10000, 'y(' + str(i) + ')')
    for j in A[i]:
        z[i, j] = model.NewIntVar(0, 1, 'z(' + str(i) + ',' + str(j) + ')')

for i in range(1, n + 1):
    y[i] = model.NewIntVar(0, 10000, 'y(' + str(i) + ')')
    
obj = model.NewIntVar(0, 100000, 'obj')

c = model.Add(y[s] == 0)
c = model.Add(x[s] == s)

for i in range(1, n + 1):
    for j in A[i]:
        a = model.NewBoolVar('a')
        model.Add(x[j] == i).OnlyEnforceIf(a)
        model.Add(x[j] != i).OnlyEnforceIf(a.Not())
        model.Add(z[i, j] == 1).OnlyEnforceIf(a)
        model.Add(z[i, j] == 0).OnlyEnforceIf(a.Not())
        model.Add(y[j] == y[i] + T[i][j]).OnlyEnforceIf(a)

    
for i in range(1, n + 1):
    model.Add(y[i] <= L)
    
for j in range(1, n + 1):
    model.Add(x[j] in A[j])

model.Add(sum(C[i][j] * z[i,j] for [i, j] in E) == obj)
model.Minimize(obj)

solver = cp_model.CpSolver()

# Giải mô hình và in kết quả
status = solver.Solve(model)
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(solver.Value(obj))
else:
    print('NO SOLUTION')