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

def monkey_math(monkey, monkeys):
    if isinstance(monkeys[monkey], int):
        return monkeys[monkey]
    else:
        left, right, op = monkeys[monkey]
        return int(op(monkey_math(left, monkeys), monkey_math(right, monkeys)))

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
print('Root yells:', monkey_math('root', monkeys) == 152)

with open('inp', mode='r') as inp:
    print('Solution...')
    data = inp.read()
    monkeys = parse_input(data)
    print('Root yells:', monkey_math('root', monkeys))