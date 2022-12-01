print('Day 1 of Advent of Code!')

test_data = '''1000
2000
3000

4000

5000
6000

7000
8000
9000

10000'''

def calculate_calories(raw_calories):
    raw_elves = raw_calories.split('\n\n')
    elves = []
    for elf in raw_elves:
        score = sum(int(cal) for cal in elf.split('\n'))
        elves.append(score)
    return elves

def best_elf(elves):
    return max(elves)

def top_n_elves(elves, n):
    top_n = sorted(elves, reverse=True)[:n]
    return sum(top_n)


print('Testing...')
elves = calculate_calories(test_data)
print('Top elf:', best_elf(elves) == 24000)
print('Top 3 elves:', top_n_elves(elves, 3) == 45000)

print('Solution...')
with open('inp', mode='r') as inp:
    elves = calculate_calories(inp.read())
    print('Top elf:', best_elf(elves))
    print('Top 3 elves:', top_n_elves(elves, 3))
