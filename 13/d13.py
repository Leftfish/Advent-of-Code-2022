from functools import cmp_to_key, reduce
from itertools import zip_longest
from json import loads
from operator import mul

print('Day 13 of Advent of Code!')

DIVIDERS = [[[2]], [[6]]]
 
def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        if a < b: 
            return True
        elif a > b: 
            return False
        else:
            pass
 
    elif isinstance(a, list) and isinstance(b, list):
        pairs = zip_longest(a, b)
        for pair in pairs:
            if pair[0] == None: 
                return True
            elif pair[1] == None: 
                return False
            else:
                res = compare(pair[0], pair[1])
                if res != None:
                    return res

    elif isinstance(a, int) and isinstance(b, list):
        return compare([a], b)
        
    elif isinstance(a, list) and isinstance(b, int):
        return compare(a, [b])
        
def get_pairs(raw_data):
    raw_pairs = raw_data.split('\n\n')
    pairs = []
    for raw_pair in raw_pairs:
        data = raw_pair.split('\n')
        pairs.append((loads(data[0]),loads(data[1])))
    return pairs

def sum_proper_packets(pairs):
    return sum(idx for idx, pair in enumerate(pairs, start=1) if compare(*pair))

def get_decoder_key(pairs):
    def comparator(a, b):
        if compare(a, b):
            return 1
        elif not compare(a, b):
            return -1
        return 0
    
    elements = [*DIVIDERS]
    for pair in pairs:
        elements.extend(list(pair))
    
    indices = [idx for idx, packet in enumerate(sorted(elements, key=cmp_to_key(comparator), reverse=True), start=1) if packet in DIVIDERS]
    return reduce(mul, indices, 1)

test_data = '''[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]'''

print('Testing...')
pairs = get_pairs(test_data)
print('Sum of indices of proper pairs:', sum_proper_packets(pairs) == 13)
print('Decoder key:', get_decoder_key(pairs) == 140)

with open('inp', mode='r') as inp:
    print('Solution...')
    pairs = get_pairs(inp.read())
    print('Sum of indices of proper pairs:', sum_proper_packets(pairs))
    print('Decoder key:', get_decoder_key(pairs))
