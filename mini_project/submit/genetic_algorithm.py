# Genetic Algorithm
import random
import time
import math
from collections import defaultdict

def read_input():
    """
    Read the input data:
    - T: number of teachers
    - N: number of classes
    - M: number of subjects
    - Classes' subjects, Teachers' subjects, and Periods for each subject
    """
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


def generate_individual(classes, teachers, subjects, periods):
    schedule = []
    for cls in range(1, len(classes) + 1):
        for sub in classes[cls]:
            if not subjects[sub]:
                continue
            start = 6 * random.randint(0, 9) + random.randint(1, 7 - periods[sub])  # Random starting time
            teacher = random.choice(subjects[sub])
            schedule.append((cls, sub, start, teacher))
    return schedule


def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child = parent1[:point] + parent2[point:]
    return child


def mutate(individual, classes, teachers, subjects, periods):
    idx = random.randint(0, len(individual) - 1)
    cls, sub, start, teacher = individual[idx]
    new_start = 6 * random.randint(0, 9) + random.randint(1, 7 - periods[sub])
    new_teacher = random.choice(subjects[sub])
    individual[idx] = (cls, sub, new_start, new_teacher)


def select_population(population, classes, teachers, periods, population_size):
    # Sort population by fitness score (highest first)
    fitness_scores = [(individual, evaluate(individual, classes, teachers, periods)[0]) for individual in population]
    fitness_scores.sort(key=lambda x: x[1], reverse=True)

    # Select the top individuals based on fitness
    selected = [x[0] for x in fitness_scores[:population_size]]
    return selected


def genetic_algorithm(classes, teachers, subjects, periods, population_size=100, generations=700, mutation_rate=0.1):
    # Initial population
    population = [generate_individual(classes, teachers, subjects, periods) for _ in range(population_size)]
    
    for gen in range(generations):
        # Select the top two individuals as parents
        fitness_scores = [(individual, evaluate(individual, classes, teachers, periods)[0]) for individual in population]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        parent1 = fitness_scores[0][0]  # Best individual
        parent2 = fitness_scores[1][0]  # Second-best individual
        
        current_fitness, conflicting_idxs = evaluate(parent1, classes, teachers, periods)

        # Crossover to generate offspring
        next_population = []
        while len(next_population) < population_size:
            child = crossover(parent1, parent2)
            if random.random() < mutation_rate:
                mutate(child, classes, teachers, subjects, periods)
            next_population.append(child)

        population = next_population
        
        print("Generation:", gen + 1, ", Score:", current_fitness, ", conflicts:", len(conflicting_idxs))

    # Evaluate and return the best solution
    best_schedule = max(population, key=lambda ind: evaluate(ind, classes, teachers, periods)[0])
    best_score, idxs = evaluate(best_schedule, classes, teachers, periods)
    return best_schedule, best_score, idxs


# Main execution
if __name__ == "__main__":
    # Read input data
    T, N, M, classes, teachers, subjects, periods = read_input()

    # Run the Genetic Algorithm
    start_time = time.time()
    schedule, score, idxs = genetic_algorithm(classes, teachers, subjects, periods)
    end_time = time.time()
    
    # Output the best schedule and the score
    print(score)
    for idx in range(len(schedule)):
        if idx not in idxs:
            cls, sub, start, teacher = schedule[idx]
            print(cls, sub, start, teacher)

    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.4f} seconds")
