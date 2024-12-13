from ortools.linear_solver import pywraplp
import sys

def input():
    [n] = [int(x) for x in sys.stdin.readline().split()]
    X = []
    for i in range(n):
        c = [int(x) for x in sys.stdin.readline().split()]
        X.append(c)
    return n, X

n, X = input()

if n <= 20 :

    # create solver
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # define decision variables
    x =  [[solver.IntVar(0, 1, 'x(' + str(i) + ',' + str(j) + ')') for i in range(n)] for j in range(n)]

    y = [solver.IntVar(0, 0, 'y(0)')] + [solver.IntVar(1, n - 1, 'y(' + str(i) + ')') for i in range(1, n)]

    z = solver.IntVar(0, solver.infinity(), 'z')

    # state constraints
    for i in range(1, n):
        for j in range(1, n):
            if (i != j) : 
                r = solver.Constraint(-solver.infinity(), n - 1)
                r.SetCoefficient(y[i], 1)
                r.SetCoefficient(y[j], -1)
                r.SetCoefficient(x[i][j], n)

    for i in range(n):
        c = solver.Constraint(1,1)
        for j in range(n):
            if (i != j) :
                c.SetCoefficient(x[i][j], 1)
            
    for j in range(n):
        c = solver.Constraint(1,1)
        for i in range(n):
            if (i != j):
                c.SetCoefficient(x[i][j], 1)

    s = solver.Constraint(0,0)
    s.SetCoefficient(z,-1)
    for i in range(n):
        for j in range(n):
            if (i != j):
                s.SetCoefficient(x[i][j], X[i][j])

    obj = solver.Objective()
    obj.SetCoefficient(z, 1)
    obj.SetMinimization()

    status = solver.Solve()

    if status != pywraplp.Solver.OPTIMAL:
        print (-1)
    else:
        print(n)
        tmp = 0
        for i in range(n):
            print(tmp + 1, end = " ")
            for j in range(n):
                if (x[tmp][j].solution_value() > 0.5):
                    tmp = j
                    break

else:
    x = [0] * n
    x_opt = [0] * n
    check = [0] * n
    nearest = [0] * n
    f_min = float('inf')

    # nearest[i]: đỉnh chưa được duyệt gần đỉnh i nhất
    # check[i]: kiểm tra xem đỉnh i đã được duyệt chưa

    # Lặp qua từng đỉnh xuất phát s
    for s in range(n):
        # Khởi tạo check[] = 0
        check = [0] * n

    # Khởi tạo giá trị nhỏ nhất tạm thời = 0
    min_tmp = 0

    # Khởi tạo đỉnh xuất phát là s
    x[0] = s
    check[s] = 1

    # Tìm đỉnh chưa duyệt gần nhất với đỉnh hiện tại
    for i in range(n - 1):
        k = x[i]
        min_val = float('inf')
        for j in range(n):
            if check[j] == 1 or k == j:
                continue
            if X[k][j] < min_val:
                min_val = X[k][j]
                nearest[k] = j

        x[i + 1] = nearest[k]
        min_tmp += min_val
        check[x[i + 1]] = 1

    # Tính khoảng cách từ đỉnh cuối về đỉnh đầu
    min_tmp += X[x[n - 1]][x[0]]

    # Cập nhật f_min và x_opt nếu tìm được hành trình ngắn hơn
    if min_tmp < f_min:
        f_min = min_tmp
        for i in range(n):
            x_opt[i] = x[i]

    # In ra kết quả
    print(n)
    for i in range(n):
        print(x_opt[i] + 1, end=" ")  # Chuyển từ chỉ số 0-based sang 1-based