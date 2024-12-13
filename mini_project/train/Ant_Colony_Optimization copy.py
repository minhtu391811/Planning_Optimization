import random
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

def generate_solution(T, N, classes, teachers, subjects, periods, pheromones, alpha=1.0, beta=2.0):
    schedule = []
    available_slots = [(session, start) for session in range(10) for start in range(1, 7)]

    assigned_classes = defaultdict(list)
    assigned_teachers = defaultdict(list)
    
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
                        if any(start_period <= s < start_period + d or s <= start_period < s + periods[su] for (su, s) in assigned_classes[cls]):
                            continue
                        if any(start_period <= s < start_period + d or s <= start_period < s + periods[su] for (su, s) in assigned_teachers[teacher]):
                            continue
                        pheromone = pheromones[(cls, sub, start_period, teacher)]
                        heuristic = 1.0 / len(teachers[teacher])
                        probabilities.append((cls, sub, start_period, teacher, pheromone ** alpha * heuristic ** beta))

            total = sum(p for *_, p in probabilities)
            if total == 0:
                continue
            probabilities = [(c, s, st, t, p / total) for c, s, st, t, p in probabilities]
            choice = random.choices(probabilities, weights=[p for *_, p in probabilities], k=1)[0]
            start, teacher = choice[2], choice[3]
            schedule.append((cls, sub, start, teacher))
            assigned_classes[cls].append((sub, start))
            assigned_teachers[teacher].append((sub, start))

    return schedule

def update_pheromones(pheromones, schedule_score, decay=0.5, Q=10.0):
    for key in pheromones.keys():
        pheromones[key] *= (1 - decay)
    for schedule in schedule_score:
        for (cls, sub, start, teacher) in schedule:
            pheromones[(cls, sub, start, teacher)] += len(schedule)

def ant_colony_optimization(T, N, M, classes, teachers, subjects, periods, num_ants=10, iterations=100):
    pheromones = defaultdict(lambda: 0.1)
    best_schedule = []
    best_score = 0

    for _ in range(iterations):
        schedule_score = []
        for _ in range(num_ants):
            schedule = generate_solution(T, N, classes, teachers, subjects, periods, pheromones)
            if len(schedule) > best_score:
                best_schedule = schedule
                best_score = len(schedule)
            schedule_score.append(schedule)

        update_pheromones(pheromones, schedule_score)

    return best_schedule, best_score

# Main execution
if __name__ == "__main__":
    # Read input data
    T, N, M, classes, teachers, subjects, periods = read_input()

    # Run Ant Colony Optimization
    schedule, score = ant_colony_optimization(T, N, M, classes, teachers, subjects, periods)

    # Output the best schedule and the score
    print(score)
    for cls, sub, start, teacher in schedule:
        print(cls, sub, start, teacher)