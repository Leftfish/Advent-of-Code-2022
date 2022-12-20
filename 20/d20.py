print('Day 20 of Advent of Code!')

class Node:
    def __init__(self, value):
        self.prv = None
        self.nxt = None
        self.value = value
    
    def __repr__(self):
        return f'V: {self.value}'

    def move(self):
        steps = self.value
        if steps:
            # wypięcie obecnego ogniwa
            self.nxt.prv = self.prv
            self.prv.nxt = self.nxt

            # znalezienie następnego
            current = self
            
            if steps > 0:
                for _ in range(abs(steps)):
                    current = current.nxt
                new_nxt = current.nxt
                current.nxt = self
                self.prv = current
                self.nxt = new_nxt
                new_nxt.prv = self
            elif steps < 0:
                for _ in range(abs(steps)):
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

def mix(nodes):
    for node in nodes:
        node.move()
    
def get_coordinates(start):
    first = traverse(start, 1000)
    second = traverse(first, 1000)
    third = traverse(second, 1000)
    return first.value + second.value + third.value

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
print(get_coordinates(start))


with open('inp', mode='r') as inp:
    print('Solution...')
    raw = list(map(int, inp.read().splitlines()))
    nodes, start = setup_nodes(raw)
    #mix(nodes)
    #print(get_coordinates(start))
    