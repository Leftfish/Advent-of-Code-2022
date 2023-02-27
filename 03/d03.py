print('Day 3 of Advent of Code!')

SCORES = {}

for i in range(ord('A'), ord('z') + 1):
    SCORES[chr(i)] = i - 38 if chr(i).isupper() else i - 96

def calculate_rucksacks_priority(line):
    rucksack_border = len(line)//2
    first, second, *rest = set(line[:rucksack_border]), set(line[rucksack_border:])
    common_element = (first & second).pop()
    return SCORES[common_element]
    
def calculate_total_priorities(raw_data):
    return sum(calculate_rucksacks_priority(line) for line in raw_data.splitlines())

def make_groups(lines, size):
    return [lines[i:i+size] for i in range(0, len(lines), size)]

def calculate_badge(rucksacks):
    first, second, third, *rest = [set(rucksack) for rucksack in rucksacks]
    badge = ((first & second) & third).pop()
    return SCORES[badge]

def calculate_total_badges(raw_data, size):
    return sum(calculate_badge(group) for group in make_groups(raw_data.splitlines(), size))

test_data = '''vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw'''

print('Testing...')
print('Rucksack priorities:', calculate_total_priorities(test_data) == 157)
print('Badge priorities:', calculate_total_badges(test_data, 3) == 70)

print('Solution...')
with open('inp.dat', mode='r') as inp:
    raw_data = inp.read()
    print('Rucksack priorities:', calculate_total_priorities(raw_data))
    print('Badge priorities:', calculate_total_badges(raw_data, 3))
