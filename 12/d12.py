from collections import defaultdict, deque

print('Day 12 of Advent of Code!')

START = ord('S')
LOW = ord('a')
END = ord('E')
LAST = ord('z')
STEP = 1

class Graph:
    def __init__(self, data):
        def is_in_board(i, j):
            return len(data) > i >= 0 and len(data[0]) > j >= 0
        
        self.heights = data
        self.edges = defaultdict(list)
        self.start, self.end = None, None
        
        for i in range(len(data)):
            for j in range(len(data[0])):
                for neighbor in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                    if is_in_board(*neighbor):
                        current_height = data[i][j]

                        if current_height == START:
                            self.start = (i, j)
                        elif current_height == END:
                            self.end = (i, j)
                        
                        neighbor_height = data[neighbor[0]][neighbor[1]]
                        diff = neighbor_height - current_height
                        
                        if (ord('a') - ord('z')) < diff <= STEP or \
                            current_height == START or (current_height == LAST and neighbor_height == END):
                            self.edges[(i, j)].append(neighbor)
                        
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

# this should just look from 'E' to closest 'a' but I'm too sleepy to implement it
def find_shortest_from_lowest(graph):
    shortest = float('inf')
    for i in range(len(graph.heights)):
        for j in range(len(graph.heights[0])):
            if graph.heights[i][j] in (START, LOW):
                graph.find_distances((i, j))
                cost = graph.distances.get(graph.end, float('inf'))
                if cost < shortest:
                    shortest = cost
    return shortest

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
print('Shortest distance from S or any a:', find_shortest_from_lowest(G) == 29)

with open('inp', mode='r') as inp:
    print('Solution...')
    data = [list(map(ord, list(line))) for line in inp.read().splitlines()]
    G = Graph(data)
    G.find_distances(G.start)
    print('Shortest distance from S:', G.distances[G.end])
    print('Shortest distance from S or any a:', find_shortest_from_lowest(G))