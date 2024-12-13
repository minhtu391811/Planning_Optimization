# Simulated Annealing
import random
import time
import sys
import math
from collections import defaultdict

def read_input():
    """
    Đọc dữ liệu đầu vào từ người dùng theo định dạng:
    - Dòng đầu: T, N, M (số giáo viên, lớp học, môn học)
    - Tiếp theo N dòng: Danh sách các môn mà lớp i cần phải học, kết thúc bởi 0
    - Tiếp theo T dòng: Danh sách các môn mà giáo viên t có thể dạy, kết thúc bởi 0
    - Cuối cùng: Danh sách số tiết của mỗi môn d(m) (m = 1, ..., M)
    """

    # Đọc số lượng giáo viên, lớp, môn
    [T, N, M] = [int(i) for i in sys.stdin.readline().split()]

    # Đọc danh sách môn học của mỗi lớp
    classes = {}
    for i in range(1, N + 1):
        data = [int(i) for i in sys.stdin.readline().split()]
        classes[i] = data[:-1] # bỏ số 0 cuối

    # Đọc danh sách môn học mà mỗi giáo viên có thể dạy
    teachers = {}
    # Danh sách giáo viên có thể dạy môn học
    subjects = defaultdict(list)
    for i in range(1, T + 1):
        data = [int(i) for i in sys.stdin.readline().split()]
        teachers[i] = data[:-1] # bỏ số 0 cuối
        for sub in teachers[i]:
            subjects[sub].append(i)

    # Đọc số tiết của mỗi môn
    periods = defaultdict(list)
    data = [int(i) for i in sys.stdin.readline().split()]
    for i in range(1, M + 1):
        periods[i] = data[i - 1]

    return T, N, M, classes, teachers, subjects, periods

T, N, M, classes, teachers, subjects, periods = read_input()

# Định nghĩa hàm đánh giá
def evaluate(schedule, classes, teachers, periods):
    score = 0
    assigned_classes = defaultdict(list)
    assigned_teachers = defaultdict(list)
    idxs = []
    for idx in range(len(schedule)):
        (cls, sub, start, teacher) = schedule[idx]
        d = periods[sub]
        # Kiểm tra chồng lấn thời khóa biểu trong cùng lớp hoặc cùng giáo viên
        if any(start <= s < start + d or s <= start < s + periods[su] for (su, s) in assigned_classes[cls]):
            idxs.append(idx)
            continue
             
        if any(start <= s < start + d or s <= start < s + periods[su] for (su, s) in assigned_teachers[teacher]):
            idxs.append(idx)
            continue

        assigned_classes[cls].append((sub, start))
        assigned_teachers[teacher].append((sub, start))
        score += 1
    return score, idxs

# Tìm kiếm lân cận
def select_neighbor(schedule, classes, teachers, periods, selected_idxs, T):
    current_score, idxs = evaluate(schedule, classes, teachers, periods)
    new_schedule = schedule[:]
    idx = random.choice(selected_idxs)
    cls, sub, start, teacher = new_schedule[idx]
    
    # Thay đổi ngẫu nhiên lớp, môn, giáo viên hoặc thời gian bắt đầu
    new_start = 6 * random.randint(0, 9) + random.randint(1, 7 - periods[sub])
    new_teacher = random.choice(subjects[sub])
    new_schedule[idx] = (cls, sub, new_start, new_teacher)
    new_score, idxs = evaluate(new_schedule, classes, teachers, periods)
    
    if new_score > current_score:
        return new_schedule
    else:
        prob = math.exp(-(new_score - current_score) / T);
        
        if random.randint(0, 1) < prob:
            return new_schedule
        else: 
            return schedule

# Thuật toán Simulated Annealing
def simulated_annealing(classes, teachers, subjects, periods, max_iterations = 10000, temp=100):
    # Tạo lịch khởi tạo ban đầu
    schedule = []
    idx = 1
    for cls in range(1, N + 1):
        for sub in classes[cls]:
            start = 6 * random.randint(0, 9) + random.randint(1, 7 - periods[sub])
            if not subjects[sub]:
                continue
            teacher = random.choice(subjects[sub])
            schedule.append((cls, sub, start, teacher))
    
    max_score = len(schedule)
    current_score, selected_idxs = evaluate(schedule, classes, teachers, periods)
    
    for _ in range(max_iterations):
        if not selected_idxs:
            continue
        new_schedule = select_neighbor(schedule, classes, teachers, periods, selected_idxs, temp)
        new_score, selected_idxs = evaluate(new_schedule, classes, teachers, periods)
        if new_score > current_score:
            schedule = new_schedule
            current_score = new_score
            
        if current_score == max_score:
            break
            
        if temp > 0.01:
            temp *= 0.99  # Giảm nhiệt độ

    return schedule, current_score, selected_idxs

# Bắt đầu đo thời gian
start_time = time.time()

schedule, score, seleted_idxs = simulated_annealing(classes, teachers, subjects, periods)
score, selected_idxs = evaluate(schedule, classes, teachers, periods)

# Kết thúc đo thời gian
end_time = time.time()
elapsed_time = end_time - start_time

print(score)
# print("Schedule:")
for idx in range(len(schedule)):
    if idx not in seleted_idxs:
        cls, sub, start, teacher = schedule[idx]
        print(cls, sub, start, teacher)
# print(f"Elapsed time: {elapsed_time:.4f} seconds")