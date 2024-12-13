from GA import genetic_algorithm
from util import fitness
from collections import defaultdict
import sys

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

    return T, N, M, classes, subjects, periods

def print_schedule(individual, d):
    score = 0
    assigned_classes = defaultdict(list)
    assigned_teachers = defaultdict(list)

    for idx, class_schedule_list in individual.items():
        for subject in class_schedule_list:
            subject_id, start_period, teacher = subject
            duration = d[subject_id]

            # Kiểm tra chồng lấn thời khóa biểu trong cùng lớp
            if any(start_period <= s < start_period + duration or s <= start_period < s + duration for (sub, s) in assigned_classes[idx]):
                continue

            # Kiểm tra chồng lấn thời khóa biểu trong cùng giáo viên
            if any(start_period <= s < start_period + duration or s <= start_period < s + duration for (sub, s) in assigned_teachers[teacher]):
                continue

            # Nếu không có chồng lấn, cập nhật lịch cho lớp và giáo viên
            assigned_classes[idx].append((subject_id, start_period))
            assigned_teachers[teacher].append((subject_id, start_period))
            print(idx, subject_id, start_period, teacher)
            score += 1

if __name__ == '__main__':
    population_size = 8
    generations = 10000

    T, N, M, subjects_per_class, teachers_per_subject, d = read_input()

    best_individual = genetic_algorithm(N, generations, population_size, subjects_per_class, teachers_per_subject, T, d)

    # Output
    K = fitness(best_individual, T, d, subjects_per_class, teachers_per_subject)
    print(K)
    print_schedule(best_individual, d)
