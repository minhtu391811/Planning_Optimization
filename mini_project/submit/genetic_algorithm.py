import random
import time
from collections import defaultdict

# Initiate parameters
POPULATION_SIZE = 100
MAX_GENERATION = 1000
MUTATION_RATE = 0.5
TIME_LIMIT = 20

# Input function to read input data
def read_input():
    """
    Read the input data:
    - T: number of teachers
    - N: number of classes
    - M: number of subjects
    - Classes' subjects, Teachers' subjects, and Periods for each subject
    """
    [T, N, M] = [int(i) for i in input().split()]
    
    # Reading classes' subject data
    classes = {}
    for i in range(1, N + 1):
        data = [int(i) for i in input().split()]
        classes[i] = data[:-1]  # Remove the trailing zero

    # Reading teachers' subject data and building a subject-to-teachers mapping
    teachers = {}
    subjects = defaultdict(list)
    for i in range(1, T + 1):
        data = [int(i) for i in input().split()]
        teachers[i] = data[:-1]
        for sub in teachers[i]:
            subjects[sub].append(i)  # Link subject to available teachers

    # Reading the duration (periods) for each subject
    periods = {}
    data = [int(i) for i in input().split()]
    for i in range(1, M + 1):
        periods[i] = data[i - 1]

    return T, N, M, classes, teachers, subjects, periods

# Evaluation function the fitness of a schedule
def evaluate(schedule, classes, teachers, periods):
    """
    Evaluate the fitness of a schedule:
    - Checks for conflicts in class schedules and teacher availability.
    - Returns the score and list of conflicting indices.
    """
    score = 0  # Initialize fitness score
    assigned_classes = defaultdict(list)  # Tracks assigned time slots for each class
    assigned_teachers = defaultdict(list)  # Tracks assigned time slots for each teacher
    idxs = []  # List of conflicting schedule indices

    for idx in range(len(schedule)):
        (cls, sub, start, teacher) = schedule[idx]
        d = periods[sub]  # Duration of the subject
        
        # Check for conflicts in the class schedule
        if any(start <= s < start + d or s <= start < s + periods[su] for (su, s) in assigned_classes[cls]):
            idxs.append(idx)
            continue
        
        # Check for conflicts in the teacher's schedule
        if any(start <= s < start + d or s <= start < s + periods[su] for (su, s) in assigned_teachers[teacher]):
            idxs.append(idx)
            continue

        # Assign subject to the class and teacher if no conflicts exist
        assigned_classes[cls].append((sub, start))
        assigned_teachers[teacher].append((sub, start))
        score += 1  # Increment fitness score
    
    return score, idxs

# Function to generate a random individual schedule
def generate_individual(classes, teachers, subjects, periods):
    """
    Generate a random schedule (individual) for the genetic algorithm:
    - Randomly assigns start times and teachers for each subject.
    """
    schedule = []
    for cls in range(1, len(classes) + 1):
        for sub in classes[cls]:
            if not subjects[sub]:  # Skip if no teacher is available for the subject
                continue
            # Random starting time within allowed range
            start = 6 * random.randint(0, 9) + random.randint(1, 7 - periods[sub])
            # Randomly select a teacher for the subject
            teacher = random.choice(subjects[sub])
            schedule.append((cls, sub, start, teacher))  # Add to the schedule
    return schedule

# Function to perform crossover between two parents
def crossover(parent1, parent2):
    """
    Perform single-point crossover between two parent schedules:
    - Combines segments of two schedules to produce an offspring.
    """
    point = random.randint(1, len(parent1) - 1)  # Random crossover point
    child = parent1[:point] + parent2[point:]  # Combine segments
    return child

# Function to mutate an individual
def mutate(individual, classes, teachers, subjects, periods):
    """
    Mutate an individual by changing the start time or teacher of a random subject.
    """
    idx = random.randint(0, len(individual) - 1)  # Select a random position in the schedule
    cls, sub, start, teacher = individual[idx]
    # Assign a new random start time
    new_start = 6 * random.randint(0, 9) + random.randint(1, 7 - periods[sub])
    # Assign a new random teacher for the subject
    new_teacher = random.choice(subjects[sub])
    individual[idx] = (cls, sub, new_start, new_teacher)

# Function to select the best individuals for the next generation
def select_population(population, classes, teachers, periods, population_size):
    """
    Select the top individuals based on their fitness scores.
    """
    # Calculate fitness for each individual
    fitness_scores = [(individual, evaluate(individual, classes, teachers, periods)[0]) for individual in population]
    # Sort population by fitness (highest first)
    fitness_scores.sort(key=lambda x: x[1], reverse=True)
    # Return the top individuals
    selected = [x[0] for x in fitness_scores[:population_size]]
    return selected

# Genetic Algorithm function
def genetic_algorithm(classes, teachers, subjects, periods, start_time, population_size=POPULATION_SIZE, generations=MAX_GENERATION, mutation_rate=MUTATION_RATE):
    """
    Run the genetic algorithm to find the optimal schedule.
    """
    # Generate initial population
    population = [generate_individual(classes, teachers, subjects, periods) for _ in range(population_size)]
    
    for gen in range(generations):
        # Evaluate the fitness of the current population
        fitness_scores = [(individual, evaluate(individual, classes, teachers, periods)[0]) for individual in population]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)  # Sort individuals by fitness
        
        # Select the best two individuals as parents
        parent1 = fitness_scores[0][0]
        parent2 = fitness_scores[1][0]
        
        current_fitness, conflicting_idxs = evaluate(parent1, classes, teachers, periods)
        end_time = time.time()
        
        # Termination condition: no conflicts or time limit exceeded
        if not conflicting_idxs or end_time - start_time > TIME_LIMIT:
            break

        # Generate next generation through crossover and mutation
        next_population = []
        while len(next_population) < population_size:
            child = crossover(parent1, parent2)  # Crossover
            if random.random() < mutation_rate:
                mutate(child, classes, teachers, subjects, periods)  # Apply mutation
            next_population.append(child)

        population = next_population  # Update population
        
        print("Generation:", gen + 1, ", Score:", current_fitness, ", conflicts:", len(conflicting_idxs))

    # Return the best individual from the final generation
    best_schedule = max(population, key=lambda ind: evaluate(ind, classes, teachers, periods)[0])
    best_score, idxs = evaluate(best_schedule, classes, teachers, periods)
    return best_schedule, best_score, idxs

# Main execution
if __name__ == "__main__":
    # Read input data
    T, N, M, classes, teachers, subjects, periods = read_input()

    # Run the Genetic Algorithm
    start_time = time.time()
    schedule, score, idxs = genetic_algorithm(classes, teachers, subjects, periods, start_time)
    end_time = time.time()
    
    # Output the best schedule and the score
    print(score)
    for idx in range(len(schedule)):
        if idx not in idxs:  # Only print valid (non-conflicting) schedules
            cls, sub, start, teacher = schedule[idx]
            print(cls, sub, start, teacher)

    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.4f} seconds")
