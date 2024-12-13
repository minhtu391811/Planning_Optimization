import math
import random

# Parameters
mutate_prob = 0.05  # Small probability with which mutation will occur.
max_generations = 10000  # Limit on generations to avoid infinite loops.

class Population:
    def __init__(self, pop_size, board_size):
        self.pop_size = pop_size
        self.board_size = board_size
        self.population_list = []
        self.fitness_list = []
        self.pos_bits_size = int(math.ceil(math.log(board_size, 2))) + 1
        self.indv_size = board_size * self.pos_bits_size

    def genPopulation(self):
        """Generates a population of lists to solve the N-Queen problem."""
        self.population_list = []
        for _ in range(self.pop_size):
            individual = [0] * self.indv_size
            for j in range(self.board_size):
                vert_pos = random.randint(0, self.board_size - 1)
                vert_pos_bitnum = toBitList(vert_pos, self.pos_bits_size)
                for k in range(self.pos_bits_size):
                    individual[j * self.pos_bits_size + k] = vert_pos_bitnum[k]
            self.population_list.append(individual)

    def computeFitnessList(self, fitnessFunction):
        """Populates the fitness list with fitness function values of corresponding entries in the population list."""
        self.fitness_list = []
        cmlsum = 0
        for individual in self.population_list:
            cmlsum += fitnessFunction(individual, self.board_size, self.pos_bits_size)
            self.fitness_list.append(cmlsum)

    def findInFitnessList(self, key):
        """Binary Search for finding appropriate index for key in fitness list."""
        low, high = 0, len(self.fitness_list) - 1
        while low <= high:
            mid = (low + high) // 2
            if key > self.fitness_list[mid]:
                low = mid + 1
            elif key < self.fitness_list[mid]:
                high = mid - 1
            else:
                return mid
        return low

def toBitList(number, size):
    """Converts a number to a list of bits of length 'size', in binary representation."""
    bit_list = [0] * size
    idx = size - 1
    while number > 0:
        bit_list[idx] = number % 2
        number //= 2
        idx -= 1
    return bit_list

def fromBitList(bit_list):
    """Converts a list of bits in binary format to a decimal number."""
    number = 0
    for bit in bit_list:
        number = (number << 1) | bit
    return number

def fitnessFunction(individual, board_size, pos_bits_size):
    """Calculates and returns the fitness value of an individual."""
    right_diag = [0] * (2 * board_size - 1)
    left_diag = [0] * (2 * board_size - 1)
    vertical = [0] * board_size
    conflicts = 0
    for idx in range(board_size):
        vpos = fromBitList(individual[idx * pos_bits_size : (idx + 1) * pos_bits_size])
        if vertical[vpos] != 0:
            conflicts += vertical[vpos]
        vertical[vpos] += 1
        if left_diag[vpos + idx] != 0:
            conflicts += left_diag[vpos + idx]
        left_diag[vpos + idx] += 1
        if right_diag[vpos + board_size - idx - 1] != 0:
            conflicts += right_diag[vpos + board_size - idx - 1]
        right_diag[vpos + board_size - idx - 1] += 1
    return (board_size * (board_size - 1)) // 2 - conflicts

def geneticAlgorithm(population, fitnessFunction):
    """Main genetic algorithm for solving the N-Queens problem."""
    generation = 0
    while generation < max_generations:
        population.computeFitnessList(fitnessFunction)
        new_pop = []
        for _ in range(len(population.population_list)):
            parent_x, parent_y = randomSelection(population)
            child = reproduce(parent_x, parent_y, population)
            if mutate_prob > random.random():
                mutate(child, population)
            new_pop.append(child)
        population.population_list = new_pop
        generation += 1
        if fitnessFunction(child, population.board_size, population.pos_bits_size) == (population.board_size * (population.board_size - 1)) // 2:
            return child
    return None  # No solution found within max_generations

def randomSelection(population):
    rand_sel_x = random.randint(1, population.fitness_list[-1])
    parent_x_idx = population.findInFitnessList(rand_sel_x)
    range_rem = population.fitness_list[parent_x_idx]
    if rand_sel_x > population.fitness_list[0]:
        range_rem -= population.fitness_list[parent_x_idx - 1]
    rand_sel_y = random.randint(1, population.fitness_list[-1] - range_rem)
    if rand_sel_y >= rand_sel_x:
        rand_sel_y += range_rem
    parent_y_idx = population.findInFitnessList(rand_sel_y)
    return population.population_list[parent_x_idx], population.population_list[parent_y_idx]

def reproduce(parent_x, parent_y, population):
    crossover_pt = random.randint(1, population.board_size - 1)
    return parent_x[:crossover_pt * population.pos_bits_size] + parent_y[crossover_pt * population.pos_bits_size:]

def mutate(child, population):
    rand_idx = random.randint(0, population.board_size - 1)
    rand_vpos = random.randint(0, population.board_size - 1)
    temp_bitnum = toBitList(rand_vpos, population.pos_bits_size)
    for i in range(population.pos_bits_size):
        child[rand_idx * population.pos_bits_size + i] = temp_bitnum[i]

# Main execution block
if __name__ == "__main__":
    pop_size = int(input("Enter population size: "))
    board_size = int(input("Enter board size (N): "))
    new_pop = Population(pop_size, board_size)
    new_pop.genPopulation()
    result = geneticAlgorithm(new_pop, fitnessFunction)

    if result:
        print("Solution found:")
        for i in range(board_size):
            print(fromBitList(result[i * new_pop.pos_bits_size : (i + 1) * new_pop.pos_bits_size]) + 1, end=" ")
    else:
        print("No solution found within the maximum generations.")
