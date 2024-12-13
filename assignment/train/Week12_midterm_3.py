import sys

def read_input():
    [n, m] = [int(n) for n in sys.stdin.readline().split()]
    E = []
    Adj = {}
    for i in range(1, n + 1):
        Adj[i] = []
    for _ in range(m):
        [u, v, w] = [int(i) for i in sys.stdin.readline().split()]
        E.append([u, v, w])
        E.append([v, u, w])
        Adj[u].append(v)
        Adj[v].append(u)
    s = [int(s) for s in sys.stdin.readline().split()]
    K = [int(k) for k in sys.stdin.readline().split()]
    data = [int(data) for data in sys.stdin.readline().split()]
    T = []
    for val in data:
        T.append(val)
    return n, m, s, K, E, T, Adj

# Input
n, m, s, K, E, T, Adj = read_input()

# Initialize the distance matrix S (Floyd-Warshall)
S = {}
for i in range(1, n + 1):
    S[i, i] = 0  # Distance to itself is 0

for i in range(1, n + 1):
    for j in range(1, n + 1):
        if i!=j: S[i,j] = 1000000

# Initialize the graph edges into the distance matrix
for u, v, w in E:
    S[u, v] = min(S[u, v], w)  # In case there are multiple edges, take the minimum
    S[v, u] = min(S[v, u], w)

# Floyd-Warshall Algorithm
for k in range(1, n + 1):
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if S[i, j] > S[i, k] + S[k, j]:
                S[i, j] = S[i, k] + S[k, j]

# Now we need to find the shortest paths between the vertices in T.
# We will track the edges used for these paths.
vertex = []
edges = []

def find_subset():
    global vertex, edges
    T_list = list(T)
    end_node = 0
    shortest_length = float('inf')

    vertex.append(s)  # Starting node s
    while T_list:
        for t in T:
            if t in T_list:
                # Find the shortest path from any vertex in vertex list to t
                for u in vertex:
                    path_length = S[u, t]
                    if path_length < shortest_length:
                        end_node = t
                        shortest_length = path_length
                        last = u

        T_list.remove(end_node)
        vertex.append(end_node)
        edges.append([last, end_node])

# Find shortest paths among the set T
find_subset()

# Print the edges used in the shortest paths
print("Edges used in shortest paths:", edges)
