import random
import time
import math
import statistics
from collections import defaultdict
from tabulate import tabulate  # Thư viện hiển thị bảng

def read_input(file_path):
    """
    Read input data from a file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    T, N, M = map(int, lines[0].split())

    # Classes' subject requirements
    classes = {i: list(map(int, lines[i].split()))[:-1] for i in range(1, N + 1)}

    # Teachers' capabilities and subjects they can teach
    teachers = {}
    subjects = defaultdict(list)
    for t in range(1, T + 1):
        data = list(map(int, lines[N + t].split()))[:-1]
        teachers[t] = data
        for sub in data:
            subjects[sub].append(t)

    # Periods required for each subject
    periods = {i + 1: int(p) for i, p in enumerate(map(int, lines[-1].split()))}

    return T, N, M, classes, teachers, subjects, periods

def evaluate(schedule, periods):
    """
    Evaluate the schedule for overlaps.
    Returns a score, list of conflicting indices, and assigned schedules.
    """
    assigned_classes = defaultdict(list)
    assigned_teachers = defaultdict(list)
    conflicting_idxs = []

    for idx, (cls, sub, start, teacher) in enumerate(schedule):
        duration = periods[sub]

        # Check for class conflicts
        if any(not (start >= s + periods[su] or s >= start + duration) for su, s in assigned_classes[cls]):
            conflicting_idxs.append(idx)
            continue

        # Check for teacher conflicts
        if any(not (start >= s + periods[su] or s >= start + duration) for su, s in assigned_teachers[teacher]):
            conflicting_idxs.append(idx)
            continue

        # Assign the schedule if no conflicts
        assigned_classes[cls].append((sub, start))
        assigned_teachers[teacher].append((sub, start))

    score = len(schedule) - len(conflicting_idxs)
    return score, conflicting_idxs

def select_neighbor(schedule, subjects, periods, conflicting_idxs, temperature):
    """
    Generate a neighbor schedule by resolving conflicts.
    """
    new_schedule = schedule[:]
    if random.random() < 0.5:
        idx = random.choice(conflicting_idxs)
    else:
        idx = random.randint(0, len(schedule) - 1)
    cls, sub, _, _ = new_schedule[idx]

    # Generate new start time and teacher
    new_start = 6 * random.randint(0, 9) + random.randint(1, 7 - periods[sub])
    new_teacher = random.choice(subjects[sub])
    new_schedule[idx] = (cls, sub, new_start, new_teacher)

    return new_schedule

def simulated_annealing(classes, subjects, periods, start_time, max_iterations=10000, initial_temp=100):
    """
    Perform Simulated Annealing to optimize the schedule.
    """
    schedule = []
    for cls, subjects_list in classes.items():
        for sub in subjects_list:
            if sub not in periods or not subjects[sub]:
                continue
            start = 6 * random.randint(0, 9) + random.randint(1, 7 - periods[sub])
            teacher = random.choice(subjects[sub])
            schedule.append((cls, sub, start, teacher))

    max_score = len(schedule)
    current_score, conflicting_idxs = evaluate(schedule, periods)
    temp = initial_temp

    for it in range(max_iterations):
        end_time = time.time()
        if not conflicting_idxs or end_time - start_time > 20.0:
            break

        new_schedule = select_neighbor(schedule, subjects, periods, conflicting_idxs, temp)
        new_score, new_conflicting_idxs = evaluate(new_schedule, periods)

        if new_score > current_score or random.random() < math.exp((new_score - current_score) / temp):
            schedule, current_score, conflicting_idxs = new_schedule, new_score, new_conflicting_idxs

        temp *= 0.999  # Cooling schedule

    return schedule, current_score

# Main Execution
if __name__ == "__main__":
    num_files = 10  # Number of input files
    scores_summary = []

    for i in range(1, num_files + 1):
        file_path = f"F:/ITTN - Project/Planning_Optimization/mini_project/test_case/data{i}.txt"
        T, N, M, classes, teachers, subjects, periods = read_input(file_path)

        scores = []
        num_runs = 10  # Number of runs per dataset

        for _ in range(num_runs):
            start_time = time.time()
            _, score = simulated_annealing(classes, subjects, periods, start_time)
            scores.append(score)

        max_score = max(scores)
        min_score = min(scores)
        mean_score = statistics.mean(scores)
        std_dev = statistics.stdev(scores) if len(scores) > 1 else 0

        scores_summary.append([f"data{i}.txt", max_score, min_score, mean_score, round(std_dev,2)])

    # Print results in a table
    print("\n=== Results Summary ===")
    print(tabulate(scores_summary, headers=["Dataset", "Max Score", "Min Score", "Average Score", "Std Dev"]))
