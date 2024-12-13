import sys

# Đọc dữ liệu đầu vào
def input_data():
    n = int(input())
    c = []
    for i in range(n):
        c.append([int(x) for x in input().split()])
    return n, c

n, c = input_data()

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
            if c[k][j] < min_val:
                min_val = c[k][j]
                nearest[k] = j

        x[i + 1] = nearest[k]
        min_tmp += min_val
        check[x[i + 1]] = 1

    # Tính khoảng cách từ đỉnh cuối về đỉnh đầu
    min_tmp += c[x[n - 1]][x[0]]

    # Cập nhật f_min và x_opt nếu tìm được hành trình ngắn hơn
    if min_tmp < f_min:
        f_min = min_tmp
        for i in range(n):
            x_opt[i] = x[i]

# In ra kết quả
print(n)
for i in range(n):
    print(x_opt[i] + 1, end=" ")  # Chuyển từ chỉ số 0-based sang 1-based
