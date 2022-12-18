from collections import deque

print('Day 18 of Advent of Code!')

def setup_cubes(data):
    cubes = set()
    for line in data.splitlines():
        coords = tuple(map(int, line.split(',')))
        cubes.add(coords)
    return cubes

def setup_grid(cubes):
    grid = set()
    min_x, max_x = 0, 0
    min_y, max_y = 0, 0
    min_z, max_z = 0, 0
    for cube in cubes:
        x, y, z = cube
        min_x = min(x, min_x)
        max_x = max(x, max_x)
        min_y = min(y, min_y)
        max_y = max(y, max_y)
        min_z = min(z, min_z)
        max_z = max(z, max_z)
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            for z in range(min_z, max_z+1):
                location = (x,y,z)
                grid.add(location)
    return grid

def get_adjacent(x, y, z):
    adjacents = set()
    deltas = (-1, 1)
    for delta in deltas:
        for position in range(3):
            adjacent = [x, y, z]
            adjacent[position] += delta
            adjacents.add(tuple(adjacent))    
    return adjacents

def check_exposure(cubes):
    exposed = {cube: 6 for cube in cubes}
    for cube in cubes:
        adjacents = get_adjacent(*cube)
        exposed[cube] -= len(cubes & adjacents)
    return exposed

def fill_with_air(grid, cubes, start = (0,0,0)):
    Q = deque()
    filled = set()

    Q.append(start)
    
    while Q:
        current = Q.popleft()
        filled.add(current)
        adjacents = get_adjacent(*current)
        for adjacent in adjacents:
            if adjacent in grid and adjacent not in cubes and adjacent not in filled:
                filled.add(adjacent)
                Q.append(adjacent)
    return filled

test_data = '''2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5'''

print('Testing...')
cubes = setup_cubes(test_data)
grid = setup_grid(cubes)
exposed_surface = check_exposure(cubes)
filled = fill_with_air(grid, cubes)
pockets_surface = check_exposure(grid - (filled | cubes))
print('Total exposed:', sum(exposed_surface.values()) == 64)
print('Exposed without trapped pockets:', sum(exposed_surface.values()) - sum(pockets_surface.values()) == 58)

with open('inp', mode='r') as inp:
    print('Solution...')
    raw_data = inp.read()
    cubes = setup_cubes(raw_data)
    grid = setup_grid(cubes)
    exposed_surface = check_exposure(cubes)
    filled = fill_with_air(grid, cubes)
    pockets_surface = check_exposure(grid - (filled | cubes))
    print('Total exposed:', sum(exposed_surface.values()))
    print('Exposed without trapped pockets:', sum(exposed_surface.values()) - sum(pockets_surface.values()))