from collections import defaultdict, deque
from itertools import combinations
import re

print('Day 16 of Advent of Code!')

REGEX = r'Valve (\w+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.+)'

class Valve:
    def __init__(self, name, flow, neighbor_ids):
        self.name = name
        self.flow = flow
        self.neighbor_ids = neighbor_ids
        self.neighbors = []
        self.distances = {}

    def __repr__(self):
        return f'{self.name}/{str(self.flow)}'

    def find_immediate_neighbors(self, valves):
        for valve in valves:
            if valve != self and valve.name in self.neighbor_ids:
                self.neighbors.append(valve)
                self.distances[valve] = 1

    def find_shortest(self):
        distances = {self: 0}
        visited = set()

        pq = deque([[0, self]])
        
        while pq:
            _, current = pq.popleft()
            visited.add(current)

            for neighbor in current.neighbors:
                if neighbor not in visited:
                    old_cost = distances.get(neighbor, float('inf'))
                    new_cost = distances[current] + 1
                    if new_cost < old_cost:
                        pq.append([new_cost, neighbor])
                        distances[neighbor] = new_cost
        self.distances = distances

    def modify_distances(self):
        distances = {k: v for k, v in self.distances.items()}
        for target in self.distances:
            if target == self or target.flow == 0: # remove distances to self or not important valves
                del distances[target]
            else:                                  # add +1 for time to open valve
                 distances[target] += 1
        self.distances = distances

def parse_data(data):
    valves = []
    for line in data.splitlines():
        name, flow, neighbors = re.findall(REGEX, line)[0]
        valves.append(Valve(name, int(flow), neighbors.split(', ')))
    return valves

def get_valves(data):
    valves = parse_data(data)
    for valve in valves:
        valve.find_immediate_neighbors(valves)
    for valve in valves:
        valve.find_shortest()
        valve.modify_distances()
    return valves

sum_psi = lambda open_valves, time: sum((valve.flow * (time - open_valves[valve])) for valve in open_valves if open_valves[valve] < 30)

def go_alone(start, usable_valves, max_time=30):
    max_score = 0
    winning = []
    solutions = {}
    stack = []
    initial_state = ([start], 0, {}, 0)
    stack.append(initial_state)

    while stack:
        current = stack.pop()
        visited, time, open_valves, score = current
        state_score = sum_psi(open_valves, max_time)
        solutions[tuple(visited)] = state_score
        if time >= max_time or len(visited) - 1 == len(usable_valves):
            if state_score > max_score:
                max_score = state_score
                winning = (visited, open_valves)
        else:
            for valve in usable_valves:
                if valve not in visited:
                    new_visited = visited.copy()
                    new_visited.append(valve)

                    new_time = time + visited[-1].distances[valve]

                    new_open_valves = {k: v for k, v in open_valves.items()}
                    new_open_valves[valve] = new_time

                    new_score = sum_psi(new_open_valves, new_time)

                    new_state = (new_visited, new_time, new_open_valves, new_score)
                    if new_time <= max_time:
                        stack.append(new_state)

    return solutions, max_score, winning[0]

def go_with_elephant(start, usable_valves, max_time=26):
    viable_solutions = defaultdict(int)
    max_score = 0
    my_path = None
    elephant_path = None

    solutions, _, __ = go_alone(start, usable_valves, max_time)
    
    for solution in solutions:
        valves = frozenset(solution)
        score = solutions[solution]
        if score > viable_solutions[valves]:
            viable_solutions[valves] = score

    for me, elephant in combinations(viable_solutions, 2):
        if len(me & elephant) == 1:
            score = viable_solutions[me] + viable_solutions[elephant]
            if score > max_score:
                max_score = score
                my_path, elephant_path = me, elephant

    return max_score, my_path, elephant_path


test_data = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II'''

print('Testing...')
valves = get_valves(test_data)
AA = [valve for valve in valves if valve.name == 'AA'].pop()
usable_valves = [valve for valve in valves if valve.flow > 0]
_, max_score, path = go_alone(AA, usable_valves, 30)
max_with_elephant, my_path, elephant_path = go_with_elephant(AA, usable_valves, 26)
print(f'Max score if you go alone: {max_score}.')
print(f'Max score if you go with the elephant: {max_with_elephant}.')

with open('inp.dat', mode='r') as inp:
    print('Solution...')
    valves = get_valves(inp.read())
    AA = [valve for valve in valves if valve.name == 'AA'].pop()
    usable_valves = [valve for valve in valves if valve.flow > 0]
    _, max_score, path = go_alone(AA, usable_valves, 30)
    max_with_elephant, my_path, elephant_path = go_with_elephant(AA, usable_valves, 26)
    print(f'Max score if you go alone: {max_score}.')
    print(f'Max score if you go with the elephant: {max_with_elephant}.')
