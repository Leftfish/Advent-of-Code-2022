print('Day 6 of Advent of Code!')

def check(data, step):
    for i in range(len(data)):
        chunk = data[i:i+step]
        if len(chunk) == len(set(chunk)):
            return i + step

print('Testing...')
test_data = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'
print("Marker:", check(test_data, 4) == 7)
print("Message:", check(test_data, 14)  == 19)

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    print("Marker:", check(raw_data, 4))
    print("Message:", check(raw_data, 14))