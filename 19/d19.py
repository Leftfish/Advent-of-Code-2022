import re
from collections import defaultdict, deque
from operator import mul
from functools import reduce

print('Day 19 of Advent of Code')

WAIT_MINE = 'pass'
ORE = 'ore'
CLAY = 'clay'
OBSIDIAN = 'obsidian'
GEODE = 'geode'
PROBES = 'probes'
RESOURCES = [ORE, CLAY, OBSIDIAN, GEODE]

REGEX = r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.'

def get_blueprints(data):
    blueprints = {}
    for line in data.splitlines():
        numbers = list(map(int, re.findall(REGEX, line).pop()))
        blueprint = {}
        id = numbers[0]
        blueprints[id] = blueprint
        blueprint[PROBES] = {}
        blueprint[PROBES][ORE] = {ORE: numbers[1], CLAY: 0, OBSIDIAN: 0}
        blueprint[PROBES][CLAY] = {ORE: numbers[2], CLAY: 0, OBSIDIAN: 0}
        blueprint[PROBES][OBSIDIAN] = {ORE: numbers[3], CLAY: numbers[4], OBSIDIAN: 0}
        blueprint[PROBES][GEODE] = {ORE: numbers[5], CLAY: 0, OBSIDIAN: numbers[6]}
        blueprint[PROBES][WAIT_MINE] = {ORE: 0, CLAY: 0, OBSIDIAN: 0}
    return blueprints

def get_moves(resources, blueprint):
    moves = set()
    for possible_move in blueprint[PROBES]:
        needed = blueprint[PROBES][possible_move]
        enough = all([needed[resource] <= resources[resource] for resource in needed])
        if enough:
            moves.add(possible_move)
    return moves

def build_more_probes(probes, resources, blueprint, move):
    new_probes = {probe: qty for probe, qty in probes.items()}
    new_resources = {resource: qty for resource, qty in resources.items()}
    new_probes[move] += 1
    for resource, qty in blueprint[PROBES][move].items():
        new_resources[resource] -= qty
    return new_probes, new_resources
            
def not_enough_minerals(probes, resources):
    new_resources = {resource: qty for resource, qty in resources.items()}
    for robot, qty in probes.items():
        new_resources[robot] += qty
    return new_resources

def play_aoc_starcraft(blueprint, max_time):
    t = 0
    probes = {ORE: 1, CLAY: 0, OBSIDIAN: 0, GEODE: 0}
    resources = {ORE: 0, CLAY: 0, OBSIDIAN: 0, GEODE: 0}
    ignored_from_last = set()
    initial_state = (t, probes, resources, ignored_from_last)
    
    max_needed_probes = {resource: 0 for resource in RESOURCES}
    for robot in blueprint[PROBES]:
        for resource, qty in blueprint[PROBES][robot].items():
            max_needed_probes[resource] = max(max_needed_probes[resource], qty) 
    max_needed_probes[GEODE] = float('inf')

    scores = defaultdict(int)

    q = deque([initial_state])

    while q:
        t, probes, resources, ignored_from_last = q.popleft()
        
        if resources[GEODE] > scores[t]:
            scores[t] = resources[GEODE]
        
        if t < max_time and scores[t] == resources[GEODE]:
            moves = get_moves(resources, blueprint)
            for move in moves:
                if move == WAIT_MINE:
                    new_resources = not_enough_minerals(probes, resources)
                    new_probes = {probe: qty for probe, qty in probes.items()}
                    new_state = (t+1, new_probes, new_resources, moves)
                    q.append(new_state)
                elif probes[move] + 1 > max_needed_probes[move] or move in ignored_from_last:
                    continue
                else:
                    new_probes, spent_resources = build_more_probes(probes, resources, blueprint, move)
                    new_resources = not_enough_minerals(probes, spent_resources)
                    new_state = (t+1, new_probes, new_resources, set())
                    q.appendleft(new_state)
    return scores[max_time]

test_data = '''Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.'''

print('Testing...')
blueprints = get_blueprints(test_data)
print('Quality index for 24 minutes:', sum(blueprint_id * play_aoc_starcraft(blueprints[blueprint_id], 24) for blueprint_id in blueprints) == 33)
with open('inp.dat', mode='r') as inp:
    print('Solution...')
    blueprints = get_blueprints(inp.read())
    print('Quality index for 24 minutes:', sum(blueprint_id * play_aoc_starcraft(blueprints[blueprint_id], 24) for blueprint_id in blueprints))
    print('Maximum for 32 minutes:', reduce(mul, [play_aoc_starcraft(blueprints[blueprint_id], 32) for blueprint_id in (1, 2, 3)], 1))

# with thanks to DrunkHacker (https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0wtmjq/?utm_source=reddit&utm_medium=web2x&context=3)
# whose implementation helped me figure out why mine did not work efficiently (I shamelessly used the idea of tracking geodes in a dictionary, which made the difference)