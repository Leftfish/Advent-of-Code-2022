from operator import add, sub, mul, truediv

print('Day 21 of Advent of Code!')

OPS = {'+': add, '-': sub, '*': mul, '/': truediv}

def parse_input(data):
    monkeys = {}
    for monkey in data.splitlines():
        name, content = monkey.split(': ')
        if content.isdigit():
            monkeys[name] = int(content)
        else:
            tokens = content.split()
            monkeys[name] = (tokens[0], tokens[2], OPS[tokens[1]])
    return monkeys

def is_human_in_branch(monkey, monkeys):
    if monkey == 'humn':
        return True
    if isinstance(monkeys[monkey], int):
        return False
    else:
        left, right, _ = monkeys[monkey]
        return is_human_in_branch(left, monkeys) or is_human_in_branch(right, monkeys)

def monkey_math(monkey, monkeys):
    if isinstance(monkeys[monkey], int):
        return monkeys[monkey]
    else:
        left, right, op = monkeys[monkey]
        return int(op(monkey_math(left, monkeys), monkey_math(right, monkeys)))

def what_should_human_scream(monkey_leader, monkeys, target):
    left, right = 0, 10000000000000
    while left < right:
        monkeys['humn'] = (left + right) // 2
        if monkeys['humn'] == right - 1 and monkey_math(monkey_leader, monkeys) != target:
            left, right = 0, 10000000000000
            while left < right:
                monkeys['humn'] = (left + right) // 2
                if monkey_math(monkey_leader, monkeys) > target:
                    right = monkeys['humn']
                elif monkey_math(monkey_leader, monkeys) < target:
                    left = monkeys['humn'] + 1
                elif monkey_math(monkey_leader, monkeys) == target:
                    return monkeys['humn']
        elif monkey_math(monkey_leader, monkeys) < target:
            right = monkeys['humn']
        elif monkey_math(monkey_leader, monkeys) > target:
            left = monkeys['humn'] + 1
        elif monkey_math(monkey_leader, monkeys) == target:
            return monkeys['humn']
        
test_data = '''root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32'''

print('Testing...')
monkeys = parse_input(test_data)
monkey_leader = monkeys['root'][0] if is_human_in_branch(monkeys['root'][0], monkeys) else monkeys['root'][1]
target = monkey_math(monkeys['root'][0], monkeys) if monkey_leader == monkeys['root'][1] else monkey_math(monkeys['root'][1], monkeys)
print('Root yells:', monkey_math('root', monkeys) == 152)
print('Human yells:', what_should_human_scream(monkey_leader, monkeys, target) == 301)

with open('inp', mode='r') as inp:
    print('Solution...')
    monkeys = parse_input(inp.read())
    monkey_leader = monkeys['root'][0] if is_human_in_branch(monkeys['root'][0], monkeys) else monkeys['root'][1]
    target = monkey_math(monkeys['root'][0], monkeys) if monkey_leader == monkeys['root'][1] else monkey_math(monkeys['root'][1], monkeys)
    print('Root yells:', monkey_math('root', monkeys))
    print('Human yells:', what_should_human_scream(monkey_leader, monkeys, target))