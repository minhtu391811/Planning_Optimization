from ortools.sat.python import cp_model
import sys

# Function to read input
def read_input():
    # Read number of variables
    n = int(sys.stdin.readline())
    domains = []  # List to store domain of each variable

    # Read domain of each variable
    for i in range(n):
        data = sys.stdin.readline().split()
        k = int(data[0])  # Number of values in the domain of Xi
        domains.append([int(v) for v in data[1:]])  # Store the values in the domain of Xi
    
    # Read number of constraints
    m = int(sys.stdin.readline())
    constraints = []
    for _ in range(m):
        i, j, D = map(int, sys.stdin.readline().split())
        constraints.append((i - 1, j - 1, D))  # Adjusting for 0-based index

    return n, domains, constraints

# Read the input
n, domains, constraints = read_input()

# Create the model and variables
model = cp_model.CpModel()
X = {}
for i in range(n):
    X[i] = model.NewIntVarFromDomain(cp_model.Domain.FromValues(domains[i]), f'X[{i}]')

# Add constraints
for i, j, D in constraints:
    model.Add(X[i] <= X[j] + D)

# Solution callback to print domains after finding a solution
class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables, domains):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.variables = variables
        self.domains = domains
        self.solution_count = 0

    def on_solution_callback(self):
        self.solution_count += 1
        for i, var in enumerate(self.variables):
            value = self.Value(var)
            if value not in self.domains[i]:
                self.domains[i].append(value)

# Create the solver and search for all solutions
solver = cp_model.CpSolver()
solver.parameters.search_branching = cp_model.FIXED_SEARCH
vars = [X[i] for i in range(n)]
solution_printer = VarArraySolutionPrinter(vars, [list(domain) for domain in domains])
solver.SearchForAllSolutions(model, solution_printer)

# Check for fail or print solutions
if solver.StatusName() == 'INFEASIBLE':
    print('FAIL')
else:
    for i in range(n):
        # Sort and print the domains of each variable
        sorted_domain = sorted(solution_printer.domains[i])
        print(len(sorted_domain), end=' ')
        print(' '.join(map(str, sorted_domain)))
