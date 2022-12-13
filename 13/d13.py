from json import loads
from itertools import zip_longest

print('Day 13 of Advent of Code!')
 
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

def sum_proper(pairs):
    return sum(i + 1 for i, pair in enumerate(pairs) if compare(*pair))

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
print('Sum of indices of proper pairs:', sum_proper(pairs) == 13)

with open('inp', mode='r') as inp:
    print('Solution...')
    pairs = get_pairs(inp.read())
    print('Sum of indices of proper pairs:', sum_proper(pairs))