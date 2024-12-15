#Ant Colony Optimization
import random
import time
from collections import defaultdict

def read_input():
    [T, N, M] = [int(i) for i in input().split()]

    classes = {}
    for i in range(1, N + 1):
        data = [int(i) for i in input().split()]
        classes[i] = data[:-1]  # remove the trailing zero

    teachers = {}
    subjects = defaultdict(list)
    for i in range(1, T + 1):
        data = [int(i) for i in input().split()]
        teachers[i] = data[:-1]
        for sub in teachers[i]:
            subjects[sub].append(i)

    periods = {}
    data = [int(i) for i in input().split()]
    for i in range(1, M + 1):
        periods[i] = data[i - 1]

    return T, N, M, classes, teachers, subjects, periods

def evaluate(schedule, classes, teachers, periods):
    score = 0
    assigned_classes = defaultdict(list)
    assigned_teachers = defaultdict(list)
    idxs = []

    for idx in range(len(schedule)):
        (cls, sub, start, teacher) = schedule[idx]
        d = periods[sub]
        # Check for conflicts in the class
        if any(start <= s < start + d or s <= start < s + periods[su] for (su, s) in assigned_classes[cls]):
            idxs.append(idx)
            continue
        # Check for conflicts with the teacher
        if any(start <= s < start + d or s <= start < s + periods[su] for (su, s) in assigned_teachers[teacher]):
            idxs.append(idx)
            continue

        assigned_classes[cls].append((sub, start))
        assigned_teachers[teacher].append((sub, start))
        score += 1
    return score, idxs

def generate_solution(T, N, classes, teachers, subjects, periods, pheromones, alpha=1.0, beta=0.5):
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

def update_pheromones(pheromones, schedule_score, decay=0.5):
    for key in pheromones.keys():
        pheromones[key] *= (1 - decay)
    for schedule, conflicting_idxs in schedule_score:
        for idx in range(len(schedule)):
            cls, sub, start, teacher = schedule[idx]
            if idx not in conflicting_idxs:
                pheromones[(cls, sub, start, teacher)] += float((len(schedule) - len(conflicting_idxs)) / len(schedule))
            else:
                pheromones[(cls, sub, start, teacher)] -= pheromones[(cls, sub, start, teacher)] * float(len(conflicting_idxs) / len(schedule))

def ant_colony_optimization(T, N, M, classes, teachers, subjects, periods, num_ants=10, iterations=100):
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
            
        if not conflicting_idxs:
                break
        
        print("Iteration:", it + 1, ", Score:", score, ", conflicts:", len(conflicting_idxs))
        update_pheromones(pheromones, schedule_score)

    return best_schedule

# Main execution
if __name__ == "__main__":
    # Read input data
    T, N, M, classes, teachers, subjects, periods = read_input()

    start_time = time.time()
    # Run Ant Colony Optimization
    best_schedule = ant_colony_optimization(T, N, M, classes, teachers, subjects, periods)
    best_score, conflicting_idxs = evaluate(best_schedule, classes, teachers, periods) 
    
    end_time = time.time()

    # Output the best schedule and the score
    print(best_score)
    for idx in range(len(best_schedule)):
        if idx not in conflicting_idxs:
            cls, sub, start, teacher = best_schedule[idx]
            print(cls, sub, start, teacher)
        
    elapsed_time = start_time - end_time    
    print(f"Elapsed time: {elapsed_time:.4f} seconds")
    