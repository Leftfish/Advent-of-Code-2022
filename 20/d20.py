print('Day 20 of Advent of Code!')

ENCRYPTION_KEY = 811589153

class Node:
    def __init__(self, value):
        self.prv = None
        self.nxt = None
        self.value = value
        self.encrypted_value = value
    
    def __repr__(self):
        return f'V: {self.value} | {self.encrypted_value}'

    def move(self):
        if self.value:
            # decouple a node
            self.nxt.prv = self.prv
            self.prv.nxt = self.nxt

            # find next node and reconnect it
            current = self
            
            if self.value > 0:
                for _ in range(abs(self.value)):
                    current = current.nxt
                new_nxt = current.nxt
                current.nxt = self
                self.prv = current
                self.nxt = new_nxt
                new_nxt.prv = self
            elif self.value < 0:
                for _ in range(abs(self.value)):
                    current = current.prv
                new_prv = current.prv
                current.prv = self
                self.nxt = current
                self.prv = new_prv
                new_prv.nxt = self     

def setup_nodes(raw):
    nodes = []
    start = None

    for val in raw:
        new_node = Node(val)
        nodes.append(new_node)
        if val == 0:
            start = new_node

    for pair in list(zip(nodes, nodes[1:])):
        first, second = pair
        first.nxt = second
        second.prv = first

    nodes[0].prv = nodes[-1]
    nodes[-1].nxt = nodes[0]
    
    return nodes, start

def traverse(start, hops):
    current = start
    for _ in range(hops):
        current = current.nxt
    return current

def print_list(start):
    current = start
    while True:
        print(current)
        current = current.nxt
        if current == start:
            break
    print()

def mix(nodes):
    for node in nodes:
        node.move()
    
def apply_key_and_mix(nodes, mixes):
    print('Applying crypto key...')
    for node in nodes:
        node.encrypted_value = node.value * ENCRYPTION_KEY
        node.value = node.value * ENCRYPTION_KEY % (len(nodes) - 1)
        
    for i in range(1, mixes + 1):
        mix(nodes)
        print(f'Finished mix {i}...')

def get_coordinates(start):
    first = traverse(start, 1000)
    second = traverse(first, 1000)
    third = traverse(second, 1000)
    return first.encrypted_value + second.encrypted_value + third.encrypted_value

test_data = '''1
2
-3
3
-2
0
4'''

print('Testing...')
raw = list(map(int, test_data.splitlines()))
nodes, start = setup_nodes(raw)
mix(nodes)
print('Coordinates without key:', get_coordinates(start) == 3)
nodes, start = setup_nodes(raw)
apply_key_and_mix(nodes, 10)
print('Coordinates with key:', get_coordinates(start) == 1623178306)

with open('inp', mode='r') as inp:
    print('Solution...')
    data = inp.read()
    raw = list(map(int, data.splitlines()))
    nodes, start = setup_nodes(raw)
    mix(nodes)
    print('Coordinates without key:', get_coordinates(start))
    nodes, start = setup_nodes(raw)
    apply_key_and_mix(nodes, 10)
    print('Coordinates with key:', get_coordinates(start))
