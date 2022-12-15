import re

print('Day 15 of Advent of Code!')

REGEX = r'Sensor at x=(-?[\d]+), y=(-?[\d]+): closest beacon is at x=(-?[\d]+), y=(-?[\d]+)'

def get_sensors(data):
    sensors = {}
    for line in data.splitlines():
        coords = list(map(int, re.findall(REGEX, line)[0]))
        sensor = coords[0], coords[1]
        beacon = coords[2], coords[3]
        sensors[sensor] = beacon
    return sensors

def calc_manhattan(sensor, beacon):
    return abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])

def merge_overlapping(intervals):
    intervals.sort()
    stack = [intervals[0]]
    for i in intervals[1:]:
        if stack[-1][0] <= i[0] <= stack[-1][-1]:
            stack[-1][-1] = max(stack[-1][-1], i[-1])
        else:
            stack.append(i)
    return stack

def count_occupied(sensors, target_row, part=1, min_coord=0, max_coord=float('inf')):
    occupied_range = [0, 0]
    occupied_spaces = []
    for sensor in sensors:
        beacon = sensors[sensor]
        dist_to_target_row = abs(sensor[1] - target_row)
        dist_to_beacon = calc_manhattan(sensor, beacon)
        
        if dist_to_target_row <= dist_to_beacon:
            closest_from_target_y = sensor[0]
            to_go = dist_to_beacon - dist_to_target_row
            min_x, max_x = (closest_from_target_y - to_go, closest_from_target_y + to_go)
            if part == 2:
                occupied_spaces.append([max(min_coord, min_x), min(max_x, max_coord)])
            if min_x < occupied_range[0]:
                occupied_range[0] = min_x
            if max_x > occupied_range[1]:
                occupied_range[1] = max_x
    return occupied_range, occupied_spaces

def merge_overlapping(intervals):
    intervals.sort()
    stack = [intervals[0]]
    for i in intervals[1:]:
        if stack[-1][0] <= i[0] <= stack[-1][-1]:
            stack[-1][-1] = max(stack[-1][-1], i[-1])
        else:
            stack.append(i)
    return stack

def find_tuning_frequency(sensors, max_coord):
    print('Scanning for the distress beacon. This may take a while...')
    for i in range(max_coord + 1):
        if i > 0 and i % 250_000 == 0: print(f'Checking at Y={i}')
        overlaps = merge_overlapping(count_occupied(sensors, i, part=2, max_coord=max_coord)[1])
        if len(overlaps) > 1 and overlaps[1][0] - overlaps[0][1] > 1:
            return i + 4000000 * (overlaps[0][1] + 1)

test_data = '''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3'''

print('Testing...')
sensors = get_sensors(test_data)
target_y = 10
max_coord = 20
print('Occupied positions:', sum(map(abs, count_occupied(sensors, target_y)[0])) == 26)
print('Tuning frequency:', find_tuning_frequency(sensors, max_coord) == 56000011)

with open('inp', mode='r') as inp:
    print('Solution...')
    target_y = 2_000_000
    max_coord = 4_000_000
    sensors = get_sensors(inp.read())
    print('Occupied positions:', sum(map(abs, count_occupied(sensors, target_y)[0])))
    print('Tuning frequency:', find_tuning_frequency(sensors, max_coord))

