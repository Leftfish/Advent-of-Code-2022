from collections import defaultdict, deque

print('Day 12 of Advent of Code!')

START = ord('S')
LOW = ord('a')
END = ord('E')
LAST = ord('z')
STEP = 1

class Graph:
    def __init__(self, data):
        self.heights = data
        self.edges = defaultdict(list)
        self.start, self.end = None, None
        
        for i in range(len(data)):
            for j in range(len(data[0])):
                for (adj_i, adj_j) in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                    if len(data) > adj_i >= 0 and len(data[0]) > adj_j >= 0:
                        neighbor_coords = (adj_i, adj_j)
                        current_height = data[i][j]

                        if current_height == START:
                            self.start = (i, j)
                        elif current_height == END:
                            self.end = (i, j)
                        
                        neighbor_height = data[adj_i][adj_j]
                        diff = neighbor_height - current_height
                        
                        if (ord('a') - ord('z')) < diff <= STEP or current_height == START or (current_height == LAST and neighbor_height == END):
                            self.edges[(i, j)].append(neighbor_coords)
                        
    def find_distances(self, start):
        distances = {vertex:float('inf') for vertex in self.edges}
        distances[start] = 0
        visited = set()
        
        Q = deque([start])
        
        while Q:
            current_vertex = Q.popleft()
            visited.add(current_vertex)

            for neighbor in self.edges[current_vertex]:
                if self.heights[neighbor[0]][neighbor[1]] == END:
                    distances[neighbor] = distances[current_vertex] + STEP
                    self.distances = distances
                    return                
                elif neighbor not in visited:
                    old_cost = distances.get(neighbor, float('inf'))
                    new_cost = distances[current_vertex] + STEP
                    if new_cost < old_cost:
                        Q.append(neighbor)
                        distances[neighbor] = new_cost
        
        self.distances = distances
        return

test_data = '''Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi'''

print('Testing...')
data = [list(map(ord, list(line))) for line in test_data.splitlines()]
G = Graph(data)
G.find_distances(G.start)
print('Shortest distance from S:', G.distances[G.end] == 31)

shortest_from_a = float('inf')
for i in range(len(G.heights)):
    for j in range(len(G.heights[0])):
        if G.heights[i][j] in (START, LOW):
            candidate_start = G.heights[i][j]
            G.find_distances((i, j))
            cost = G.distances.get(G.end, float('inf'))
            if cost < shortest_from_a:
                shortest_from_a = cost

print('Shortest distance from S or any a:', shortest_from_a == 29)

with open('inp', mode='r') as inp:
    print('Solution...')
    data = [list(map(ord, list(line))) for line in inp.read().splitlines()]
    G = Graph(data)
    G.find_distances(G.start)
    print('Shortest distance from S:', G.distances[G.end])

    shortest_from_a = float('inf')
    for i in range(len(G.heights)):
        for j in range(len(G.heights[0])):
            if G.heights[i][j] in (START, LOW):
                candidate_start = G.heights[i][j]
                G.find_distances((i, j))
                cost = G.distances.get(G.end, float('inf'))
                if cost < shortest_from_a:
                    shortest_from_a = cost

    print('Shortest distance from S or any a:', shortest_from_a)