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

def move(head, tail, direction, distance, visited):
    def update_tail(head_x, head_y, tail):
        tail_x, tail_y = tail
        manhattan = calc_manhattan(head_x, head_y, tail_x, tail_y)
        move = (0, 0)
        if (tail_x == head_x) and manhattan > 1:
            if head_y > tail_y:
                move = MOVE_RIGHT
            elif head_y < tail_y:
                move = MOVE_LEFT
        elif (tail_y == head_y) and manhattan > 1:
            if head_x > tail_x:
                move = MOVE_DOWN
            elif head_x < tail_x:
                move = MOVE_UP
        elif (tail_x != head_x and tail_y != head_y) and manhattan > 2:
            if head_x > tail_x and head_y > tail_y:
                move = MOVE_DOWN_RIGHT
            elif head_x > tail_x and head_y < tail_y:
                move = MOVE_DOWN_LEFT
            elif head_x < tail_x and head_y > tail_y:
                move = MOVE_UP_RIGHT
            elif head_x < tail_x and head_y < tail_y:
                move = MOVE_UP_LEFT
        dx, dy = move
        return (tail_x + dx, tail_y + dy)
    
    head_x, head_y = head
    dx, dy = direction
    for _ in range(distance):
        head_x += dx
        head_y += dy
        tail = update_tail(head_x, head_y, tail)
        visited.add(tail)
    return (head_x, head_y), tail, visited

def calc_manhattan(head_x, head_y, tail_x, tail_y):
    return abs(head_x-tail_x) + abs(head_y-tail_y)

def count_visited(data):
    head = (0, 0)
    tail = (0, 0)
    visited = set()
    moves = data.splitlines()
    for mv in moves:
        direction, distance = parse_move(mv)
        head, tail, visited = move(head, tail, direction, distance, visited)
    return len(visited)

test_data = '''R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2'''

print('Testing...')
print("Visited:", count_visited(test_data) == 13)

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    print("Visited:", count_visited(raw_data))