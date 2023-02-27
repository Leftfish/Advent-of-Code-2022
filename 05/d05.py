import re

print('Day 5 of Advent of Code!')

EMPTY = ' '
DISTANCE_CRATES = 4
MOVER9000 = 0
MOVER9001 = 1
REGEX_MOVES = r'move (\d+) from (\d) to (\d)'

def how_many_stacks(raw_data):
    for idx, line in enumerate(raw_data):
        line = line.replace(" ", "")
        if line.isnumeric():
            return idx, int(line[-1])

def make_stacks(raw_data, starting_point, number_of_stacks):
    stacks = [list() for _ in range(number_of_stacks)]
    for i in range(starting_point-1, -1, -1):
        line = raw_data[i]
        for position in range(1, len(line), DISTANCE_CRATES):
            proper_stack = position // DISTANCE_CRATES
            crate = line[position]
            if crate != EMPTY:
                stacks[proper_stack].append(crate)
    return stacks

def parse_instructions(raw_data, starting_point):
    instructions = []
    for line in raw_data[starting_point + 1:]:
        moves = re.findall(REGEX_MOVES, line)
        if moves:
            instructions.append(list(map(int, moves[0])))
    return instructions

def move_crates(stacks, instructions, version):
    for instruction in instructions:
        how_many, origin_idx, target_idx = instruction
        origin, target = stacks[origin_idx-1], stacks[target_idx-1]
        if version == MOVER9000:
            for _ in range(how_many):
                target.append(origin.pop())
        elif version == MOVER9001:
            to_move = [origin.pop() for _ in range(how_many)]
            target.extend(reversed(to_move))            
    return ''.join(stack[-1] for stack in stacks)


test_data = '''    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2'''

print('Testing...')
raw_data = test_data.splitlines()
starting_point, number_of_stacks = how_many_stacks(raw_data)
stacks = make_stacks(raw_data, starting_point, number_of_stacks)
instructions = parse_instructions(raw_data, starting_point)
print('MOVER9000:', move_crates(stacks, instructions, MOVER9000) == 'CMZ')
stacks = make_stacks(raw_data, starting_point, number_of_stacks)
print('MOVER9001:', move_crates(stacks, instructions, MOVER9001) == 'MCD')


print('Solution...')
with open('inp.dat', mode='r') as inp:
    raw_data = inp.read().splitlines()
    starting_point, number_of_stacks = how_many_stacks(raw_data)
    stacks = make_stacks(raw_data, starting_point, number_of_stacks)
    instructions = parse_instructions(raw_data, starting_point)
    print('MOVER9000:', move_crates(stacks, instructions, MOVER9000))
    stacks = make_stacks(raw_data, starting_point, number_of_stacks)
    print('MOVER9001:', move_crates(stacks, instructions, MOVER9001))