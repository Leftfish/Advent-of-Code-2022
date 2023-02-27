print('Day 14 of Advent of Code!')

DOWN = (0, 1)
DOWN_LEFT = (-1, 1)
DOWN_RIGHT = (1, 1)
MOVES = [DOWN, DOWN_LEFT, DOWN_RIGHT]
START = (500, 0)

def draw_walls(data):
    walls = set()
    for line in data.splitlines():
        pairs = [pair.split(',') for pair in line.split(' -> ')]
        wall_ranges = list(zip(pairs,pairs[1:]))
        for wall in wall_ranges:
            wall_start = list(map(int, wall[0]))
            wall_end = list(map(int, wall[1]))
            jump_x = -1 if wall_end[0] - wall_start[0] < 0 else 1
            jump_y = -1 if wall_end[1] - wall_start[1] < 0 else 1
            for x in range(wall_start[0], wall_end[0] + jump_x, jump_x):
                for y in range(wall_start[1], wall_end[1] + jump_y, jump_y):
                    walls.add((x, y))
    return walls

def drop_sand(walls, part):
    sand = set()
    sand_counter = 0
    filled = False
    lowest = max(coord[1] for coord in walls) + 2 * (part == 2)

    is_available = lambda position: position not in walls and position not in sand
    is_at_floor = lambda position: position[1] > lowest
    is_at_start = lambda position: position == START

    while not filled:
        current_position = START
        sand_counter += 1
        while current_position[1] <= lowest:
            sand_moved = False
            for move in MOVES:
                dx, dy = move
                new_position = (current_position[0] + dx, current_position[1] + dy)
                if part == 1:
                    if is_available(new_position):
                        current_position = new_position
                        sand_moved = True
                        break
                elif part == 2:
                    if is_available(new_position) and new_position[1] < lowest:
                        current_position = new_position
                        sand_moved = True
                        break
            
            if is_at_floor(current_position) or is_at_start(current_position):
                filled = True
            
            if not sand_moved:
                sand.add(current_position)
                break
            
    return sand_counter - (part == 1)

test_data = '''498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9'''

print('Testing...')
walls = draw_walls(test_data)
print('Sand to fill the walls:', drop_sand(walls, part=1) == 24)
print('Sand to reach the top:', drop_sand(walls, part=2) == 93)


with open('inp.dat', mode='r') as inp:
    print('Solution...')
    test_data = inp.read()
    walls = draw_walls(test_data)
    print('Sand to fill the walls:', drop_sand(walls, part=1))
    print('Sand to reach the top:', drop_sand(walls, part=2))
