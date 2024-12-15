import random
import time
import statistics
from collections import defaultdict
from tabulate import tabulate

# Hàm đọc dữ liệu từ file
def read_input(file_path):
    """
    Đọc dữ liệu đầu vào từ file.
    """
    with open(file_path, 'r') as file:
        [T, N, M] = [int(i) for i in file.readline().split()]

        classes = {}
        for i in range(1, N + 1):
            data = [int(i) for i in file.readline().split()]
            classes[i] = data[:-1]

        teachers = {}
        subjects = defaultdict(list)
        for i in range(1, T + 1):
            data = [int(i) for i in file.readline().split()]
            teachers[i] = data[:-1]
            for sub in teachers[i]:
                subjects[sub].append(i)

        periods = {}
        data = [int(i) for i in file.readline().split()]
        for i in range(1, M + 1):
            periods[i] = data[i - 1]

    return T, N, M, classes, teachers, subjects, periods

# Hàm đánh giá lịch trình
def evaluate(schedule, classes, teachers, periods):
    score = 0
    assigned_classes = defaultdict(list)
    assigned_teachers = defaultdict(list)
    idxs = []

    for idx in range(len(schedule)):
        (cls, sub, start, teacher) = schedule[idx]
        d = periods[sub]
        # Kiểm tra xung đột lớp học
        if any(start <= s < start + d or s <= start < s + periods[su] for (su, s) in assigned_classes[cls]):
            idxs.append(idx)
            continue
        # Kiểm tra xung đột giáo viên
        if any(start <= s < start + d or s <= start < s + periods[su] for (su, s) in assigned_teachers[teacher]):
            idxs.append(idx)
            continue

        assigned_classes[cls].append((sub, start))
        assigned_teachers[teacher].append((sub, start))
        score += 1
    return score, idxs

# Sinh lời giải
def generate_solution(T, N, classes, teachers, subjects, periods, pheromones, alpha=1.5, beta=1.5):
    schedule = []
    available_slots = [(session, start) for session in range(10) for start in range(1, 7)]

    for cls in range(1, N + 1):
        for sub in classes[cls]:
            d = periods[sub]
            if not subjects[sub]:
                continue
            probabilities = []
            for teacher in subjects[sub]:
                for slot in available_slots:
                    session, start = slot
                    if start + periods[sub] < 8:
                        start_period = session * 6 + start
                        pheromone = pheromones[(cls, sub, start_period, teacher)]
                        heuristic = 1.0 / len(teachers[teacher])
                        probabilities.append((cls, sub, start_period, teacher, pheromone ** alpha * heuristic ** beta))

            total = sum(p for *_, p in probabilities)
            if total == 0:
                continue
            probabilities = [(c, s, st, t, p / total) for c, s, st, t, p in probabilities]
            choice = random.choices(probabilities, weights=[p for *_, p in probabilities])[0]

            start_period, teacher = choice[2], choice[3]
            schedule.append((cls, sub, start_period, teacher))

    return schedule

# Cập nhật pheromone
def update_pheromones(pheromones, schedule_score, decay=0.5):
    for key in pheromones.keys():
        pheromones[key] *= (1 - decay)
    for schedule, conflicting_idxs in schedule_score:
        for idx in range(len(schedule)):
            cls, sub, start, teacher = schedule[idx]
            if idx not in conflicting_idxs:
                pheromones[(cls, sub, start, teacher)] += (len(schedule) - len(conflicting_idxs)) / len(schedule)
            else:
                pheromones[(cls, sub, start, teacher)] -= pheromones[(cls, sub, start, teacher)] * len(conflicting_idxs) / len(schedule)

# Thuật toán ACO
def ant_colony_optimization(T, N, M, classes, teachers, subjects, periods, start_time, num_ants=10, iterations=200):
    pheromones = defaultdict(lambda: 1.0)
    best_schedule = []
    best_score = 0

    for it in range(iterations):
        schedule_score = []
        conflicting_idxs = []
        score = 0
        for _ in range(num_ants):
            schedule = generate_solution(T, N, classes, teachers, subjects, periods, pheromones)
            score, conflicting_idxs = evaluate(schedule, classes, teachers, periods)
            if score > best_score:
                best_schedule = schedule
                best_score = score
            schedule_score.append((schedule, conflicting_idxs))

        end_time = time.time()
        if not conflicting_idxs or end_time - start_time > 20.0:
            break

        update_pheromones(pheromones, schedule_score)

    return best_schedule, best_score

# Hàm chạy thuật toán và tính toán kết quả
def run_ant_colony(file_path):
    T, N, M, classes, teachers, subjects, periods = read_input(file_path)
    scores = []

    for _ in range(10):
        start_time = time.time()
        schedule, score = ant_colony_optimization(T, N, M, classes, teachers, subjects, periods, start_time)
        scores.append(score)

    max_score = max(scores)
    min_score = min(scores)
    avg_score = round(statistics.mean(scores), 2)
    std_dev = round(statistics.stdev(scores), 2)

    return max_score, min_score, avg_score, std_dev

# Hàm chính tạo bảng kết quả
if __name__ == "__main__":
    results = []

    for i in range(1, 11):
        file_path = f"F:/ITTN - Project/Planning_Optimization/mini_project/test_case/data{i}.txt"
        max_score, min_score, avg_score, std_dev = run_ant_colony(file_path)
        results.append({
            "Dataset": f"data{i}",
            "Max Score": max_score,
            "Min Score": min_score,
            "Average Score": avg_score,
            "Std Dev": std_dev
        })

    print("\n=== Results Summary ===")
    print(tabulate(results, headers="keys", floatfmt=".2f"))
