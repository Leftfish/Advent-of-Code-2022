print('Day 3 of Advent of Code!')

SCORES = {}

for i in range(65, 122+1):
    if i <= 90:
        SCORES[chr(i)] = i - 38
    else:
        SCORES[chr(i)] = i - 96

def calculate_rucksacks_priority(line):
    border = len(line)//2
    first, second = set(line[:border]), set(line[border:])
    common = (first & second).pop()
    return SCORES[common]
    
def sum_prorities(raw_data):
    return sum(calculate_rucksacks_priority(line) for line in raw_data.splitlines())

def calculate_badge_priority(rucksacks):
    first, second, third, *rest = [set(rucksack) for rucksack in rucksacks]
    badge = ((first & second) & third).pop()
    return SCORES[badge]

def make_groups(lines, size):
    return [lines[i:i+size] for i in range(0, len(lines), size)]

def sum_badge_priorities(raw_data, size):
    return sum(calculate_badge_priority(group) for group in make_groups(raw_data.splitlines(), size))

test_data = '''vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw'''

print('Testing...')
print('Rucksack priorities:', sum_prorities(test_data) == 157)
print('Badge priorities:', sum_badge_priorities(test_data, 3) == 70)

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    print('Rucksack priorities:', sum_prorities(raw_data))
    print('Badge priorities:', sum_badge_priorities(raw_data, 3))