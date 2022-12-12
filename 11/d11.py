from functools import reduce
from operator import mul, add

class Monkey:
    def __init__(self, id):
        self.id = id
        self.items = set()
        self.targets = []
        self.operation = None
        self.params = ()
        self.divisibility = 1
        self.inspections_done = 0
    
    def inspect(self, item, modifier):
        self.inspections_done += 1
        param_1 = item.value if self.params[0] == 'old' else int(self.params[0])
        param_2 = item.value if self.params[1] == 'old' else int(self.params[1])
        item.value = self.operation(param_1, param_2) 
        if modifier == 3:
            item.value //= modifier
        else:
            item.value %= modifier

    def throw_to(self, item, target):
        target.items.add(item)
        self.items.remove(item)

    def check_target(self, item):
        target_index = item.value % self.divisibility != 0
        return self.targets[target_index]

    def __repr__(self):
        return f'Monkey {self.id}. Inspections: {self.inspections_done}. Items: {self.items} Targets: {self.targets} OP: {self.operation} on {self.params} Test div by: {self.divisibility}'

class Item:
    def __init__(self, value):
        self.value = value
    
def make_monkeys(data):
    id = None
    monkeys = []
    for line in data.splitlines():
        if line.startswith('Monkey'):
            new_id = int(line[-2])
            if new_id != id:
                id = new_id
                monkey = Monkey(id)
                monkeys.append(monkey)
        elif line.startswith('  Starting items'):
            _, values = line.split(': ')
            monkey.items = set([Item(int(value)) for value in values.split(', ')])
        elif line.startswith('  Operation:'):
            tokens = line.split()[-3:]
            params = (tokens[0], tokens[2])
            symbol = tokens[1]
            if symbol == '+':
                operation = add
            elif symbol == '*':
                operation = mul
            monkey.operation = operation
            monkey.params = params
        elif line.startswith('  Test'):
            monkey.divisibility = int(line.split()[-1])
        elif line.startswith('    If true'):
            monkey.targets.append(int(line.split()[-1]))
        elif line.startswith('    If false'):
            monkey.targets.append(int(line.split()[-1]))
        
    return monkeys

def simulate(monkeys, rounds, modifier):
    for _ in range(rounds):
        for monkey in monkeys:
            for item in monkey.items.copy():
                monkey.inspect(item, modifier)
                monkey.throw_to(item, monkeys[monkey.check_target(item)])
    
    inspections = sorted([m.inspections_done for m in monkeys])
    return inspections[-1] * inspections[-2]


test_data = '''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1'''

print('Testing...')
monkeys = make_monkeys(test_data)
rounds = 20
modifier = 3
print('Sane worry levels:', simulate(monkeys, rounds, modifier) == 10605)

monkeys = make_monkeys(test_data)
rounds = 10000
modifier = reduce(mul, [monkey.divisibility for monkey in monkeys], 1)
print('Insane worry levels:', simulate(monkeys, rounds, modifier) == 2713310158)

with open('inp', mode='r') as inp:
    print('Solution...')
    data = inp.read()
    monkeys = make_monkeys(data)
    rounds = 20
    modifier = 3
    print('Sane worry levels:', simulate(monkeys, rounds, modifier))

    monkeys = make_monkeys(data)
    rounds = 10000
    modifier = reduce(mul, [monkey.divisibility for monkey in monkeys], 1)
    print('Insane worry levels:', simulate(monkeys, rounds, modifier))