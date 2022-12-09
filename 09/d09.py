print('Day 9 of Advent of Code!')

MOVE_UP = (-1, 0)
MOVE_DOWN = (1, 0)
MOVE_LEFT = (0, -1)
MOVE_RIGHT = (0, 1)
MOVE_UP_RIGHT = (-1, 1)
MOVE_UP_LEFT = (-1, -1)
MOVE_DOWN_RIGHT = (1, 1)
MOVE_DOWN_LEFT = (1, -1)

MOVES = {'R': MOVE_RIGHT, 'L': MOVE_LEFT, 'U': MOVE_UP, 'D': MOVE_DOWN}

def parse_move(move):
    direction, distance = move.split()
    return MOVES[direction], int(distance)

def calc_manhattan(prev_x, prev_y, next_x, next_y):
    return abs(prev_x-next_x) + abs(prev_y-next_y)

def update_next_segment(prev_x, prev_y, next_segment):
        next_x, next_y = next_segment
        manhattan = calc_manhattan(prev_x, prev_y, next_x, next_y)
        move = (0, 0)
        if (next_x == prev_x) and manhattan > 1:
            if prev_y > next_y:
                move = MOVE_RIGHT
            elif prev_y < next_y:
                move = MOVE_LEFT
        elif (next_y == prev_y) and manhattan > 1:
            if prev_x > next_x:
                move = MOVE_DOWN
            elif prev_x < next_x:
                move = MOVE_UP
        elif (next_x != prev_x and next_y != prev_y) and manhattan > 2:
            if prev_x > next_x and prev_y > next_y:
                move = MOVE_DOWN_RIGHT
            elif prev_x > next_x and prev_y < next_y:
                move = MOVE_DOWN_LEFT
            elif prev_x < next_x and prev_y > next_y:
                move = MOVE_UP_RIGHT
            elif prev_x < next_x and prev_y < next_y:
                move = MOVE_UP_LEFT
        dx, dy = move
        return (next_x + dx, next_y + dy)

def move(bridge, direction, distance, visited):
    head_x, head_y = bridge[0]
    dx, dy = direction
    for _ in range(distance):
        head_x += dx
        head_y += dy
        bridge[0] = (head_x, head_y)
        for i in range(1, len(bridge)):
            prev_x, prev_y = bridge[i-1]
            bridge[i] = update_next_segment(prev_x, prev_y, bridge[i])
            tail = bridge[-1]
            visited.add(tail)
    return bridge, visited

def count_visited(data, bridge_length):
    bridge = [(0, 0) for _ in range(bridge_length)]    
    visited = set()
    moves = data.splitlines()
    for mv in moves:
        direction, distance = parse_move(mv)
        bridge, visited = move(bridge, direction, distance, visited)
    return len(visited)

test_data = '''R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2'''

test_data_2 = '''R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20'''

print('Testing...')
print("Visited before snap:", count_visited(test_data, 2) == 13)
print("Visited after snap:", count_visited(test_data_2, 10) == 36)

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    print("Visited before snap:", count_visited(raw_data, 2))
    print("Visited after snap:", count_visited(raw_data, 10))