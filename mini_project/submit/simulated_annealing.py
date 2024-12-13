import random
import time
import math
from collections import defaultdict

def read_input():
    """
    Read input data:
    - First line: T, N, M (number of teachers, classes, subjects)
    - Next N lines: List of subjects each class needs (ends with 0)
    - Next T lines: List of subjects each teacher can teach (ends with 0)
    - Final line: Number of periods required for each subject d(m) (m = 1, ..., M)
    """
    T, N, M = map(int, input().split())

    # Classes' subject requirements
    classes = {i: list(map(int, input().split()))[:-1] for i in range(1, N + 1)}

    # Teachers' capabilities and subjects they can teach
    teachers = {}
    subjects = defaultdict(list)
    for t in range(1, T + 1):
        data = list(map(int, input().split()))[:-1]
        teachers[t] = data
        for sub in data:
            subjects[sub].append(t)

    # Periods required for each subject
    periods = {i + 1: int(p) for i, p in enumerate(map(int, input().split()))}

    return T, N, M, classes, teachers, subjects, periods

# Optimized evaluation function
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

# Optimized neighbor selection
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

# Simulated Annealing Algorithm
def simulated_annealing(classes, subjects, periods, max_iterations=10000, initial_temp=100):
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
        if not conflicting_idxs:
            break

        new_schedule = select_neighbor(schedule, subjects, periods, conflicting_idxs, temp)
        new_score, new_conflicting_idxs = evaluate(new_schedule, periods)

        if new_score > current_score or random.random() < math.exp((new_score - current_score) / temp):
            schedule, current_score, conflicting_idxs = new_schedule, new_score, new_conflicting_idxs
            
        print("Iteration:", it + 1, ", Score:", current_score, ", conflicts:", len(conflicting_idxs))

        temp *= 0.999  # Cooling schedule

    return schedule, current_score

# Main Execution
if __name__ == "__main__":
    T, N, M, classes, teachers, subjects, periods = read_input()

    start_time = time.time()
    best_schedule, score = simulated_annealing(classes, subjects, periods)
    best_score, conflicting_idxs = evaluate(best_schedule, periods)
    elapsed_time = time.time() - start_time

    print(score)
    for idx in range(len(best_schedule)):
        if idx not in conflicting_idxs:
            cls, sub, start, teacher = best_schedule[idx]
            print(cls, sub, start, teacher)

    print(f"Elapsed time: {elapsed_time:.4f} seconds")
