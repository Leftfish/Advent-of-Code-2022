from re import findall

print('Day 4 of Advent of Code!')

REGEX = r'(\d+)-(\d+),(\d+)-(\d+)'

def parse_line(line):
    digits = tuple(map(int, findall(REGEX, line).pop()))
    first = (digits[0], digits[1])
    second = (digits[2], digits[3])
    return first, second

def check_if_contains(first, second):
    return (first[0] >= second[0] and first[1] <= second[1]) or (second[0] >= first[0] and second[1] <= first[1])

def check_if_overlaps(first, second):
    return check_if_contains(first, second) or (first[0] <= second[0] and first[1] >= second[0]) or (second[0] <= first[0] and second[1] >= first[0])

def counter(lines, checker):
    return sum(checker(*parse_line(line)) for line in lines)

test_data = '''2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8'''

print('Testing...')
raw_data = test_data.splitlines()
print('How many where one contains the other?', counter(raw_data, check_if_contains) == 2)
print('How many overlapping?', counter(raw_data, check_if_overlaps) == 4)

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.readlines()
    print('How many where one contains the other?', counter(raw_data, check_if_contains))
    print('How many overlapping?', counter(raw_data, check_if_overlaps))
