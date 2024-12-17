import random
import time
from collections import defaultdict

# Initiate parameters
NUM_ANTS = 10              # Number of ants (solutions) per iteration
ALPHA = 1.5                # Influence of pheromone level
BETA = 1.5                 # Influence of heuristic information
EVAPORATION_RATE = 0.5     # Rate at which pheromone evaporates
MAX_ITERATIONS = 200       # Maximum number of iterations
TIME_LIMIT = 20            # Time limit in seconds for the algorithm to run

# Input function to read problem data
def read_input():
    """
    Reads input data for the problem:
    - T: number of teachers
    - N: number of classes
    - M: number of subjects
    Returns:
        T, N, M, classes, teachers, subjects, periods
    """
    [T, N, M] = [int(i) for i in input().split()]  # Read T (teachers), N (classes), M (subjects)

    # Read classes and their required subjects
    classes = {}
    for i in range(1, N + 1):
        data = [int(i) for i in input().split()]
        classes[i] = data[:-1]  # Exclude trailing zero

    # Read teachers and their subjects
    teachers = {}
    subjects = defaultdict(list)  # Map each subject to its available teachers
    for i in range(1, T + 1):
        data = [int(i) for i in input().split()]
        teachers[i] = data[:-1]
        for sub in teachers[i]:
            subjects[sub].append(i)

    # Read periods required for each subject
    periods = {}
    data = [int(i) for i in input().split()]
    for i in range(1, M + 1):
        periods[i] = data[i - 1]

    return T, N, M, classes, teachers, subjects, periods

# Evaluation function to calculate score
def evaluate(schedule, classes, teachers, periods):
    """
    Evaluates a given schedule:
    - Checks for conflicts in classes and teachers' schedules.
    Returns:
        score: Total number of valid assignments
        idxs: List of indices with conflicts
    """
    score = 0
    assigned_classes = defaultdict(list)   # Tracks assigned periods for each class
    assigned_teachers = defaultdict(list)  # Tracks assigned periods for each teacher
    idxs = []  # Conflicting indices

    for idx in range(len(schedule)):
        (cls, sub, start, teacher) = schedule[idx]
        d = periods[sub]  # Duration of the subject

        # Check for conflicts in class schedules
        if any(start <= s < start + d or s <= start < s + periods[su] for (su, s) in assigned_classes[cls]):
            idxs.append(idx)
            continue
        
        # Check for conflicts in teacher schedules
        if any(start <= s < start + d or s <= start < s + periods[su] for (su, s) in assigned_teachers[teacher]):
            idxs.append(idx)
            continue

        # Update assigned schedules
        assigned_classes[cls].append((sub, start))
        assigned_teachers[teacher].append((sub, start))
        score += 1  # Increment valid assignments
    
    return score, idxs

# Function to generate solutions
def generate_solution(T, N, classes, teachers, subjects, periods, pheromones, alpha=ALPHA, beta=BETA):
    """
    Generates a solution using probabilistic selection based on pheromones and heuristics.
    Returns:
        schedule: List of valid class-subject-teacher assignments
    """
    schedule = []
    # Generate all available time slots (10 sessions with 6 possible start times)
    available_slots = [(session, start) for session in range(10) for start in range(1, 7)]
    
    for cls in range(1, N + 1):  # Loop through all classes
        for sub in classes[cls]:  # Loop through subjects required for each class
            d = periods[sub]  # Duration of subject
            if not subjects[sub]:  # Skip if no teachers can teach this subject
                continue
            
            probabilities = []  # Store probabilities for possible choices
            for teacher in subjects[sub]:  # Teachers capable of teaching this subject
                for slot in available_slots:  # All time slots
                    session, start = slot
                    if start + periods[sub] < 8:  # Ensure it fits within the session
                        start_period = session * 6 + start  # Convert to global time period
                        pheromone = pheromones[(cls, sub, start_period, teacher)]
                        heuristic = 1.0 / len(teachers[teacher])  # Favor teachers with fewer subjects
                        probabilities.append((cls, sub, start_period, teacher, pheromone ** alpha * heuristic ** beta))

            # Normalize probabilities and select based on weights
            total = sum(p for *_, p in probabilities)
            if total == 0:
                continue
            probabilities = [(c, s, st, t, p / total) for c, s, st, t, p in probabilities]
            choice = random.choices(probabilities, weights=[p for *_, p in probabilities])[0]
            
            start_period, teacher = choice[2], choice[3]
            schedule.append((cls, sub, start_period, teacher))

    return schedule

# Function to update pheromones
def update_pheromones(pheromones, schedule_score, decay=EVAPORATION_RATE):
    """
    Updates pheromone levels based on the quality of solutions.
    """
    for key in pheromones.keys():
        pheromones[key] *= (1 - decay)  # Evaporate pheromones
    
    for schedule, conflicting_idxs in schedule_score:
        for idx in range(len(schedule)):
            cls, sub, start, teacher = schedule[idx]
            if idx not in conflicting_idxs:  # Reward valid assignments
                pheromones[(cls, sub, start, teacher)] += (len(schedule) - len(conflicting_idxs)) / len(schedule)
            else:  # Penalize conflicting assignments
                pheromones[(cls, sub, start, teacher)] -= pheromones[(cls, sub, start, teacher)] * len(conflicting_idxs) / len(schedule)

# Ant Colony Optimization algorithm
def ant_colony_optimization(T, N, M, classes, teachers, subjects, periods, start_time, num_ants=NUM_ANTS, iterations=MAX_ITERATIONS):
    """
    Executes the Ant Colony Optimization algorithm.
    Returns:
        best_schedule: Schedule with the highest score
    """
    pheromones = defaultdict(lambda: 1.0)  # Initialize pheromones
    best_schedule = []
    best_score = 0

    for it in range(iterations):  # Iterate over iterations
        schedule_score = []
        conflicting_idxs = []
        score = 0

        for _ in range(num_ants):  # Generate solutions for all ants
            schedule = generate_solution(T, N, classes, teachers, subjects, periods, pheromones)
            score, conflicting_idxs = evaluate(schedule, classes, teachers, periods)

            # Update best solution
            if score > best_score:
                best_schedule = schedule
                best_score = score
            
            schedule_score.append((schedule, conflicting_idxs))
        
        end_time = time.time()
        if not conflicting_idxs or end_time - start_time > TIME_LIMIT:  # Stop early if no conflicts or time limit exceeded
            break
        
        print("Iteration:", it + 1, ", Score:", score, ", conflicts:", len(conflicting_idxs))
        update_pheromones(pheromones, schedule_score)  # Update pheromones
    
    return best_schedule

# Main execution
if __name__ == "__main__":
    # Read input data
    T, N, M, classes, teachers, subjects, periods = read_input()

    start_time = time.time()
    # Run Ant Colony Optimization
    best_schedule = ant_colony_optimization(T, N, M, classes, teachers, subjects, periods, start_time)
    best_score, conflicting_idxs = evaluate(best_schedule, classes, teachers, periods) 
    
    end_time = time.time()

    # Output the best schedule and the score
    print(best_score)
    for idx in range(len(best_schedule)):
        if idx not in conflicting_idxs:
            cls, sub, start, teacher = best_schedule[idx]
            print(cls, sub, start, teacher)
        
    elapsed_time = end_time - start_time   
    print(f"Elapsed time: {elapsed_time:.4f} seconds")
