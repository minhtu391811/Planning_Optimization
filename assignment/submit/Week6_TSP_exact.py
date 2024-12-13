# Không sử dụng binary variable

from ortools.sat.python import cp_model
import sys

def input():
    [n] = [int(x) for x in sys.stdin.readline().split()]
    X = []
    for i in range(n):
        c = [int(x) for x in sys.stdin.readline().split()]
        X.append(c)
    return n, X

n, X = input()

# create solver
model = cp_model.CpModel()
# define decision variables
x =  [model.NewIntVar(0, 1, 'x(' + str(i) + ')') for i in range(n)]

# Thêm ràng buộc: Mỗi thành phố chỉ xuất hiện một lần trong hành trình
model.AddAllDifferent(x)

# Ràng buộc: Thành phố đầu tiên phải là thành phố 1 (index 0)
model.Add(x[0] == 0)

# Tạo biến đại diện cho tổng chi phí hành trình
total_cost = model.NewIntVar(0, 1000, 'total_cost')

# Xây dựng hàm chi phí
cost_terms = []
for i in range(n - 1):
    # Tổng chi phí từ x[i] đến x[i+1]
    cost_terms.append(X[x[i]][x[i + 1]])

# Thêm chi phí từ thành phố cuối cùng trở về thành phố 1
cost_terms.append(X[x[-1]][x[0]])

# Thiết lập hàm mục tiêu là tổng chi phí
model.Add(total_cost == sum(cost_terms))
model.Minimize(total_cost)

# Tạo solver và giải bài toán
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print('Số lượng thành phố:', n)
    print('Hành trình tối ưu:', [solver.Value(x[i]) + 1 for i in range(n)])  # Cộng 1 để in ra chỉ số thành phố từ 1
    print('Tổng chi phí:', solver.Value(total_cost))
else:
    print('Không tìm thấy lời giải tối ưu.')