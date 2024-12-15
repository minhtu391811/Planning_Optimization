import random
import time
import math
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

# Tạo cá thể ban đầu
def generate_individual(classes, teachers, subjects, periods):
    schedule = []
    for cls in range(1, len(classes) + 1):
        for sub in classes[cls]:
            if not subjects[sub]:
                continue
            start = 6 * random.randint(0, 9) + random.randint(1, 7 - periods[sub])
            teacher = random.choice(subjects[sub])
            schedule.append((cls, sub, start, teacher))
    return schedule

# Hàm lai ghép (crossover)
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child = parent1[:point] + parent2[point:]
    return child

# Hàm đột biến (mutation)
def mutate(individual, classes, teachers, subjects, periods):
    idx = random.randint(0, len(individual) - 1)
    cls, sub, start, teacher = individual[idx]
    new_start = 6 * random.randint(0, 9) + random.randint(1, 7 - periods[sub])
    new_teacher = random.choice(subjects[sub])
    individual[idx] = (cls, sub, new_start, new_teacher)

# Chọn lọc dân số
def select_population(population, classes, teachers, periods, population_size):
    fitness_scores = [(individual, evaluate(individual, classes, teachers, periods)[0]) for individual in population]
    fitness_scores.sort(key=lambda x: x[1], reverse=True)
    selected = [x[0] for x in fitness_scores[:population_size]]
    return selected

# Thuật toán di truyền
def genetic_algorithm(classes, teachers, subjects, periods, start_time, population_size=100, generations=1000, mutation_rate=0.5):
    population = [generate_individual(classes, teachers, subjects, periods) for _ in range(population_size)]
    
    for gen in range(generations):
        fitness_scores = [(individual, evaluate(individual, classes, teachers, periods)[0]) for individual in population]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        parent1 = fitness_scores[0][0]  # Best individual
        parent2 = fitness_scores[1][0]  # Second-best individual
        
        current_fitness, conflicting_idxs = evaluate(parent1, classes, teachers, periods)
        end_time = time.time()
        if not conflicting_idxs or end_time - start_time > 20.0:
            break

        next_population = []
        while len(next_population) < population_size:
            child = crossover(parent1, parent2)
            if random.random() < mutation_rate:
                mutate(child, classes, teachers, subjects, periods)
            next_population.append(child)

        population = next_population
        
        print("Generation:", gen + 1, ", Score:", current_fitness, ", conflicts:", len(conflicting_idxs))

    best_schedule = max(population, key=lambda ind: evaluate(ind, classes, teachers, periods)[0])
    best_score, idxs = evaluate(best_schedule, classes, teachers, periods)
    return best_schedule, best_score, idxs

# Hàm chạy thuật toán và tính toán kết quả
def run_genetic_algorithm(file_path):
    T, N, M, classes, teachers, subjects, periods = read_input(file_path)
    scores = []

    for _ in range(10):
        start_time = time.time()
        schedule, score, idxs = genetic_algorithm(classes, teachers, subjects, periods, start_time)
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
        max_score, min_score, avg_score, std_dev = run_genetic_algorithm(file_path)
        results.append({
            "Dataset": f"data{i}",
            "Max Score": max_score,
            "Min Score": min_score,
            "Average Score": f"{avg_score:.2f}".rstrip('0').rstrip('.'),
            "Std Dev": f"{std_dev:.2f}".rstrip('0').rstrip('.')
        })

    print("\n=== Results Summary ===")
    print(tabulate(results, headers="keys", floatfmt=".2f"))
