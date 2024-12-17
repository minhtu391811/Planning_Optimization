import random
import time
import math
from collections import defaultdict

# Initiate parameters
INITIAL_TEMP = 100.0
COOLING_RATE = 0.999
MAX_ITERATION = 10000
TIME_LIMIT = 20


# Input function to read problem data
def read_input():
    """
    Read input data:
    - First line: T, N, M (number of teachers, classes, subjects)
    - Next N lines: List of subjects each class needs (ends with 0)
    - Next T lines: List of subjects each teacher can teach (ends with 0)
    - Final line: Number of periods required for each subject d(m) (m = 1, ..., M)
    """
    T, N, M = map(int, input().split())  # Number of teachers, classes, and subjects

    # Reading subject requirements for each class
    classes = {i: list(map(int, input().split()))[:-1] for i in range(1, N + 1)}

    # Reading teachers' subject capabilities and building a subject-to-teachers mapping
    teachers = {}
    subjects = defaultdict(list)
    for t in range(1, T + 1):
        data = list(map(int, input().split()))[:-1]
        teachers[t] = data  # Subjects the teacher can teach
        for sub in data:
            subjects[sub].append(t)  # Add teacher to the list of available teachers for a subject

    # Reading the number of periods required for each subject
    periods = {i + 1: int(p) for i, p in enumerate(map(int, input().split()))}

    return T, N, M, classes, teachers, subjects, periods

# Evaluation function to check for conflicts
def evaluate(schedule, periods):
    """
    Evaluate the schedule for class and teacher overlaps.
    - Returns:
        - Score: Number of non-conflicting assignments
        - List of conflicting indices
    """
    assigned_classes = defaultdict(list)  # Tracks assigned slots for each class
    assigned_teachers = defaultdict(list)  # Tracks assigned slots for each teacher
    conflicting_idxs = []  # Tracks indices of conflicting assignments

    for idx, (cls, sub, start, teacher) in enumerate(schedule):
        duration = periods[sub]  # Duration of the subject

        # Check for class conflicts
        if any(not (start >= s + periods[su] or s >= start + duration) for su, s in assigned_classes[cls]):
            conflicting_idxs.append(idx)
            continue

        # Check for teacher conflicts
        if any(not (start >= s + periods[su] or s >= start + duration) for su, s in assigned_teachers[teacher]):
            conflicting_idxs.append(idx)
            continue

        # Assign time slot to class and teacher if no conflicts exist
        assigned_classes[cls].append((sub, start))
        assigned_teachers[teacher].append((sub, start))

    # Score is the number of non-conflicting schedules
    score = len(schedule) - len(conflicting_idxs)
    return score, conflicting_idxs

# Generate a neighboring schedule by modifying conflicts
def select_neighbor(schedule, subjects, periods, conflicting_idxs, temperature):
    """
    Generate a new (neighbor) schedule by modifying a conflicting or random entry.
    - Uses random assignment for start time and teacher.
    """
    new_schedule = schedule[:]  # Create a copy of the current schedule

    # Select an index to modify: prioritize conflicts if available
    if random.random() < 0.5 and conflicting_idxs:  # Prioritize conflicts
        idx = random.choice(conflicting_idxs)
    else:
        idx = random.randint(0, len(schedule) - 1)

    cls, sub, _, _ = new_schedule[idx]

    # Generate a new random start time and teacher for the selected class/subject
    new_start = 6 * random.randint(0, 9) + random.randint(1, 7 - periods[sub])  # Random start time
    new_teacher = random.choice(subjects[sub])  # Randomly choose a teacher for the subject
    new_schedule[idx] = (cls, sub, new_start, new_teacher)  # Replace the old assignment with new values

    return new_schedule

# Simulated Annealing Algorithm
def simulated_annealing(classes, subjects, periods, start_time, max_iterations=MAX_ITERATION, initial_temp=INITIAL_TEMP):
    """
    Perform Simulated Annealing to find an optimal schedule.
    - Generates an initial random solution and improves it iteratively.
    """
    # Generate an initial random schedule
    schedule = []
    for cls, subjects_list in classes.items():
        for sub in subjects_list:
            if sub not in periods or not subjects[sub]:
                continue
            start = 6 * random.randint(0, 9) + random.randint(1, 7 - periods[sub])  # Random start time
            teacher = random.choice(subjects[sub])  # Random teacher
            schedule.append((cls, sub, start, teacher))

    # Initial evaluation
    max_score = len(schedule)
    current_score, conflicting_idxs = evaluate(schedule, periods)
    temp = initial_temp  # Starting temperature for annealing

    # Annealing loop
    for it in range(max_iterations):
        end_time = time.time()
        # Termination condition: no conflicts or time limit exceeded
        if not conflicting_idxs or end_time - start_time > TIME_LIMIT:
            break

        # Generate a new neighbor schedule
        new_schedule = select_neighbor(schedule, subjects, periods, conflicting_idxs, temp)
        new_score, new_conflicting_idxs = evaluate(new_schedule, periods)

        # Acceptance criteria: accept better solutions or probabilistically worse solutions
        if new_score > current_score or random.random() < math.exp((new_score - current_score) / temp):
            schedule, current_score, conflicting_idxs = new_schedule, new_score, new_conflicting_idxs

        # Log the progress for debugging
        print("Iteration:", it + 1, ", Score:", current_score, ", Conflicts:", len(conflicting_idxs))

        # Cooling schedule: decrease temperature
        temp *= COOLING_RATE

    return schedule, current_score

# Main Execution
if __name__ == "__main__":
    # Read input data
    T, N, M, classes, teachers, subjects, periods = read_input()

    # Run the simulated annealing algorithm
    start_time = time.time()
    best_schedule, score = simulated_annealing(classes, subjects, periods, start_time)
    best_score, conflicting_idxs = evaluate(best_schedule, periods)
    elapsed_time = time.time() - start_time

    # Print the final score and the non-conflicting schedule
    print(score)
    for idx in range(len(best_schedule)):
        if idx not in conflicting_idxs:
            cls, sub, start, teacher = best_schedule[idx]
            print(cls, sub, start, teacher)

    # Print total execution time
    print(f"Elapsed time: {elapsed_time:.4f} seconds")
