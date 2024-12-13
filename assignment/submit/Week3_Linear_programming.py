from ortools.linear_solver import pywraplp

def main():
    import sys

    # Đọc dữ liệu đầu vào
    input_lines = sys.stdin.read().splitlines()
    n, m = map(int, input_lines[0].split())
    idx = 1

    DL = []
    DU = []
    for _ in range(n):
        dl, du = map(float, input_lines[idx].split())
        DL.append(dl)
        DU.append(du)
        idx += 1

    C = list(map(float, input_lines[idx].split()))
    idx += 1

    A = []
    for _ in range(m):
        A.append(list(map(float, input_lines[idx].split())))
        idx += 1

    low = []
    up = []
    for _ in range(m):
        l, u = map(float, input_lines[idx].split())
        low.append(l)
        up.append(u)
        idx += 1

    # Tạo solver
    solver = pywraplp.Solver.CreateSolver('GLOP')  # Sử dụng solver tuyến tính

    if not solver:
        print('Solver not created.')
        return

    # Khai báo biến quyết định
    X = []
    for i in range(n):
        X.append(solver.NumVar(DL[i], DU[i], f'X[{i}]'))

    # Thêm các ràng buộc tuyến tính
    for i in range(m):
        expr = solver.Sum([A[i][j] * X[j] for j in range(n)])
        if low[i] != -100000:
            solver.Add(expr >= low[i])
        if up[i] != 100000:
            solver.Add(expr <= up[i])

    # Đặt hàm mục tiêu (tối đa hóa)
    objective = solver.Objective()
    for i in range(n):
        objective.SetCoefficient(X[i], C[i])
    objective.SetMaximization()

    # Giải bài toán
    status = solver.Solve()

    # Kiểm tra kết quả và xuất kết quả
    if status == pywraplp.Solver.OPTIMAL:
        print(n)
        result = []
        for i in range(n):
            result.append(str(X[i].solution_value()))
        print(' '.join(result))
    else:
        print('NOT_OPTIMAL')

if __name__ == '__main__':
    main()