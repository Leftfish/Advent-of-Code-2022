from enum import Enum
import heapq

print('Day 24 of Advent of Code!')

class Directions(Enum):
    N = (-1, 0)
    E = (0, 1)
    W = (0, -1)
    S = (1, 0)
    NIL = (0, 0)

class Icons(Enum):
    UP = '^'
    DOWN = 'v'
    LEFT = '<'
    RIGHT = '>'
    WALL = '#'
    FLOOR = '.'
    PLR = 'E'

BLIZZARD_MOVES = {Icons.UP.value: Directions.N, Icons.DOWN.value: Directions.S, 
                Icons.LEFT.value: Directions.W, Icons.RIGHT.value: Directions.E}

def parse_board(raw_board):
    blizzards = []
    player, finish = None, None
    for i, line in enumerate(raw_board):
        for j, char in enumerate(line):
            if i == 0:
                if raw_board[i][j] == Icons.FLOOR.value:
                    player = (i-1, 0)
                continue 
            if i == len(raw_board) - 1:
                if raw_board[i][j] == Icons.FLOOR.value:
                    finish = (i-1, j-1)
                continue
            if j == 0 or j == len(raw_board[0]) - 1:
                continue    
            if char in (Icons.UP.value, Icons.DOWN.value, Icons.LEFT.value, Icons.RIGHT.value):
                blizzard = [i-1, j-1, BLIZZARD_MOVES[char], char]
                blizzards.append(blizzard)

    board_length = len(raw_board[0]) - 2
    board_height = len(raw_board) - 2

    return blizzards, board_length, board_height, player, finish

class Basin:
    def __init__(self, blizzards, board_length, board_height, player, finish):
        self.blizzards = blizzards
        self.blizzard_positions = {}
        self.player = player
        self.start = player
        self.finish = finish
        self.score = 0
        self.board_length = board_length
        self.board_height = board_height
    
    def print(self, time):
        self.get_blizzard_positions(time)

        board = [[Icons.FLOOR.value for j in range(self.board_length)] for i in range(self.board_height)]
        for blizzard in self.blizzard_positions[time]:
            board[blizzard[0]][blizzard[1]] = '*'
        board.append([Icons.WALL.value] * self.board_length)
        
        if self.player[0] >= 0:
            board[self.player[0]][self.player[1]] = '\033[35m' + Icons.PLR.value + '\033[0m'    
        
        for line in board:
            print(''.join(line))

    def get_blizzard_positions(self, time):
        if time not in self.blizzard_positions:
            snow = set()
            for blizzard in self.blizzards:
                i = (blizzard[0] + time * blizzard[2].value[0]) % (self.board_height)
                j = (blizzard[1] + time * blizzard[2].value[1]) % (self.board_length)
                snow.add((i, j))
            self.blizzard_positions[time] = snow

    def find_possible_moves(self, player, time):
        candidates = set()
        self.get_blizzard_positions(time + 1)
        snow = self.blizzard_positions[time + 1]
        for move in (Directions.N, Directions.S, Directions.E, Directions.W, Directions.NIL):
            di, dj = move.value
            new_pos = player[0] + di, player[1] + dj
            if new_pos not in snow and (new_pos == self.start or new_pos == self.finish or 0 <= new_pos[0] < self.board_height and 0 <= new_pos[1] < self.board_length):
                candidates.add(new_pos) 
        return candidates

def setup(basin):
    visited = set()
    q = []
    heapq.heappush(q, (0, basin.player, basin.score))
    return visited, q

def reset(basin, time, player_position):
    basin.score = time
    basin.player = player_position
    basin.start, basin.finish = basin.finish, basin.start

def find_shortest_path(q, basin):
    while q:
        current = heapq.heappop(q)
        _, player_position, time = current
        if player_position == basin.finish:
            print(f'Reached goal after {time} minutes.')
            basin.score = time
            return time, player_position
        if (player_position, time) not in visited:
            visited.add((player_position, time))
            moves = basin.find_possible_moves(player_position, time)
            for move in moves:
                new_manh = abs(player_position[0]-basin.finish[0]) + abs(player_position[1] - basin.finish[1])
                new_time = time + 1
                heapq.heappush(q, (new_manh + time, move, new_time))

test_data = '''#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#'''

print('Testing...')
blizzards, board_length, board_height, player, finish = parse_board(test_data.splitlines())
B = Basin(blizzards, board_length, board_height, player, finish)
visited, q = setup(B)
time, player_position = find_shortest_path(q, B)
reset(B, time, player_position)
visited, q = setup(B)
time, player_position = find_shortest_path(q, B)
reset(B, time, player_position)
visited, q = setup(B)
time, player_position = find_shortest_path(q, B)

with open('inp.dat', mode='r') as inp:
    print('Solution...')
    blizzards, board_length, board_height, player, finish = parse_board(inp.read().splitlines())
    B = Basin(blizzards, board_length, board_height, player, finish)
    visited, q = setup(B)
    time, player_position = find_shortest_path(q, B)
    reset(B, time, player_position)
    visited, q = setup(B)
    time, player_position = find_shortest_path(q, B)
    reset(B, time, player_position)
    visited, q = setup(B)
    time, player_position = find_shortest_path(q, B)
