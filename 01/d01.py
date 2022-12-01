print('Day 1 of Advent of Code!')

def get_elf_calories(raw_elves):
    elves = []
    for elf in raw_elves:
        score = sum(int(cal) for cal in elf.split('\n'))
        elves.append(score)
    return elves

def top_n_elves(elves, n):
    top_n = sorted(elves, reverse=True)[:n]
    return sum(top_n)

def top_n_elves_one_line(raw_elves, n):
    return sum(sorted([sum(int(cal) for cal in elf.split('\n')) for elf in raw_elves])[-n:])

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


print('Testing...')
elves = get_elf_calories(test_data.split('\n\n'))
print('Top elf:', top_n_elves(elves, 1) == 24000)
print('Top 3 elves:', top_n_elves(elves, 3) == 45000)

print('Solution...')
with open('inp', mode='r') as inp:
    raw_elves = inp.read().split('\n\n')
    elves = get_elf_calories(raw_elves)
    print('Top elf:', top_n_elves(elves, 1))
    print('Top 3 elves:', top_n_elves(elves, 3))
    print(f'And the one liner works too: {top_n_elves_one_line(raw_elves, 1)} for part 1 and {top_n_elves_one_line(raw_elves, 3)} for part 2!')
