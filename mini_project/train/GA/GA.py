import numpy as np
from collections import defaultdict
from util import fitness, crossover, mutation

def create_individual(N, subjects_per_class, teachers_per_subject, d):
    individual = defaultdict(list)
    for class_id in range(1, N + 1):
        for subject_id in subjects_per_class[class_id]:
            start_period = np.random.randint(0, 10) + np.random.randint(1, 8 - d[subject_id])  # 6 periods per session
            if not teachers_per_subject[subject_id]:
                continue
            teacher = np.random.choice(teachers_per_subject[subject_id])
            individual[class_id].append([subject_id, start_period, teacher])
    return individual

def create_next_generation(parent1, parent2, population, subjects_per_class, teachers_per_subject, t, d):
    mutation_rate = 0.1
    c1, c2 = crossover(parent1, parent2)
    if np.random.uniform(0, 1) < mutation_rate:
        c1 = mutation(c1 , subjects_per_class, teachers_per_subject, d)
    if np.random.uniform(0, 1) < mutation_rate:
        c2 = mutation(c2, subjects_per_class, teachers_per_subject, d)

    population.append(c1)
    population.append(c2)

    fitness_values = [fitness(individual, t, d, subjects_per_class, teachers_per_subject) for individual in population]
    sorted_indices = np.argsort(fitness_values)[::-1]

    population = [population[i] for i in sorted_indices[:len(population) // 2]]
    return population

def genetic_algorithm(N, generations, population_size, subjects_per_class, teachers_per_subject, t, d):
    population = [create_individual(N, subjects_per_class, teachers_per_subject, d) for _ in range(population_size)]

    for _ in range(generations):
        fitness_values = [fitness(individual, t, d, subjects_per_class, teachers_per_subject) for individual in population]
        sorted_indices = np.argsort(fitness_values)[::-1]
        parent1 = population[sorted_indices[0]]
        parent2 = population[sorted_indices[1]]
        population = create_next_generation(parent1, parent2, population, subjects_per_class, teachers_per_subject, t, d)

    best_individual = max(population, key=lambda ind: fitness(ind, t, d, subjects_per_class, teachers_per_subject))
    return best_individual
