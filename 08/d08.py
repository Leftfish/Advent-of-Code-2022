from functools import reduce
from operator import mul

print('Day 8 of Advent of Code!')

def find_visible(matrix):
    visible = {}

    def look(i, start, stop, step, horizontal):
        tallest = -1
        for j in range(start, stop, step):
            if horizontal:
                current = int(matrix[i][j])
                if current > tallest:
                    visible[(i,j)] = True
                    tallest = current
            else:
                current = int(matrix[j][i])
                if current > tallest:
                    visible[(j,i)] = True
                    tallest = current
    #rows
    for i in range(len(matrix)):
        line = matrix[i]
        look(i, 0, len(line), 1, horizontal=True)
        look(i, len(line)-1, 0, -1, horizontal=True) 
    #columns    
    for i in range(len(matrix[0])):
        look(i, 0, len(matrix), 1, horizontal=False)
        look(i, len(matrix)-1, 0, -1, horizontal=False)
              
    return visible

def calculate_score(candidate, matrix):
    i, j = candidate
    
    # up, down, left, right
    score = [0, 0, 0, 0]
    
    current = matrix[i][j]
    
    # iterate up, down, left, right and see what's visible
    # no energy left to rewrite it to while loops which might be more elegant?
    
    for di in range(i-1, -1, -1):
        score[0] += 1
        if matrix[di][j] >= current:
            break
    
    for di in range(i+1, len(matrix), 1):
        score[1] += 1
        if matrix[di][j] >= current:
            break
    
    for dj in range(j-1, -1, -1):
        score[2] += 1
        if matrix[i][dj] >= current:
            break

    for dj in range(j+1, len(matrix[0]), 1):
        score[3] += 1
        if matrix[i][dj] >= current:
            break
    
    return reduce(mul, score, 1)

test_data = '''30373
25512
65332
33549
35390'''

print('Testing...')
matrix = [[chr for chr in line] for line in test_data.splitlines()]
visible = find_visible(matrix)
candidates = {(i, j): 0 for i in range(1, len(matrix[0])-1) for j in range(1, len(matrix)-1)}
scores = [calculate_score(candidate, matrix) for candidate in candidates]
print('Trees visible from the outside:', len(visible) == 21)
print('Best scenic score:', max(scores) == 8)

print('Solution...')
with open('inp.dat', mode='r') as inp:
    raw_data = inp.read()
    matrix = [[chr for chr in line] for line in raw_data.splitlines()]
    visible = find_visible(matrix)
    candidates = {(i, j): 0 for i in range(1, len(matrix[0])-1) for j in range(1, len(matrix)-1)}
    scores = [calculate_score(candidate, matrix) for candidate in candidates]
    print('Trees visible from the outside:', len(visible))
    print('Best scenic score:', max(scores))