from itertools import cycle

print('Day 22 of Advent of Code!')

UP = (-1, 0)
LEFT = (0, -1)
DOWN = (1, 0)
RIGHT = (0, 1)

WALL = '#'
VOID = ' '
FREE = '.'

PLAYER_ICON = {UP: '^', LEFT: '<', RIGHT: '>', DOWN: 'v'}
DIRECTION_SCORE = {RIGHT: 0, DOWN: 1, LEFT: 2, UP: 3}

def get_longest_line(raw_maze_lines):
    return max(len(line) for line in raw_maze_lines)

def get_proper_maze(raw_maze_lines):
    proper_maze = []
    longest = get_longest_line(raw_maze_lines)
    for line in raw_maze_lines:
        line = line.replace(' ', VOID)
        if len(line) < longest:
            line += (longest - len(line)) * VOID
        proper_maze.append(list(line))
    return proper_maze

class Player:
    def __init__(self, maze, part):
        self.directions = cycle([RIGHT, DOWN, LEFT, UP])
        self.direction = next(self.directions)
        self.moves = []
        self.maze = maze
        self.maze_width = len(self.maze[0])
        self.maze_height = len(self.maze)
        self.start = self._find_start()
        self.x, self.y = self.start
        self.part = part

        self.generate_jumps()

    def __repr__(self) -> str:
        return f'X: {self.x} Y: {self.y} DIR: {PLAYER_ICON[self.direction]}'   

    def _find_start(self):
        return (0, self.maze[0].index(FREE))

    def parse_instructions(self, moves):
        move_symbols = {'R': self.turn_right, 'L': self.turn_left}        
        stack = []
        for char in moves:
            if char.isdigit():
                stack.append(char)
            else:
                number = int(''.join(stack))
                stack.clear()
                self.moves.append(number)
                self.moves.append(move_symbols[char])
        self.moves.append(int(''.join(stack)))

    def turn_right(self):
        self.direction = next(self.directions)

    def turn_left(self):
        for _ in range(3):
            self.direction = next(self.directions)

    def do_not_turn(self):
        pass

    def turn_around(self):
        for _ in range(2):
            self.direction = next(self.directions)

    def generate_jumps(self):           
        self.borders = {
        (1,3): ([(x, 49) for x in range(150, 199+1)]), 
        (3,1): [(149, y) for y in range(50,99+1)],
        (1,5): [(x, 0) for x in range(150, 199+1)],
        (5,1): [(0, y) for y in range(50, 99+1)],
        (1,6): [(199, y) for y in range(0, 49+1)],
        (6,1): [(0, y) for y in range(100, 149+1)],
        (2,5): [(x, 0) for x in range(100, 149+1)],
        (5,2): [(x, 50) for x in range(49, -1, -1)],
        (2,4): [(100, y) for y in range(0, 49+1)],
        (4,2): [(x, 50) for x in range(50, 99+1)],
        (3,6): [(x, 99) for x in range(100, 149+1)],
        (6,3): [(x, 149) for x in range(49, -1, -1)],
        (4,6): [(x, 99) for x in range(50, 99+1)],
        (6,4): [(49, y) for y in range(100, 149+1)]
        }
        self.jump_table = {
        (1,3): (dict(zip(self.borders[(1,3)], self.borders[(3,1)])), self.turn_left),
        (3,1): (dict(zip(self.borders[(3,1)], self.borders[(1,3)])), self.turn_right),
        (1,5): (dict(zip(self.borders[(1,5)], self.borders[(5,1)])), self.turn_left),
        (5,1): (dict(zip(self.borders[(5,1)], self.borders[(1,5)])), self.turn_right),
        (1,6): (dict(zip(self.borders[(1,6)], self.borders[(6,1)])), self.do_not_turn),
        (6,1): (dict(zip(self.borders[(6,1)], self.borders[(1,6)])), self.do_not_turn),
        (2,5): (dict(zip(self.borders[(2,5)], self.borders[(5,2)])), self.turn_around),
        (5,2): (dict(zip(self.borders[(5,2)], self.borders[(2,5)])), self.turn_around),
        (2,4): (dict(zip(self.borders[(2,4)], self.borders[(4,2)])), self.turn_right),
        (4,2): (dict(zip(self.borders[(4,2)], self.borders[(2,4)])), self.turn_left),
        (3,6): (dict(zip(self.borders[(3,6)], self.borders[(6,3)])), self.turn_around),
        (6,3): (dict(zip(self.borders[(6,3)], self.borders[(3,6)])), self.turn_around),
        (4,6): (dict(zip(self.borders[(4,6)], self.borders[(6,4)])), self.turn_left),
        (6,4): (dict(zip(self.borders[(6,4)], self.borders[(4,6)])), self.turn_right)
        }

    def get_current_border(self):
        candidate_borders = [border for border in self.borders if (self.x, self.y) in self.borders[border]]

        if len(candidate_borders) > 1:
                if set(candidate_borders) == {(1,3), (1,6)}:
                    if self.direction == RIGHT:
                        current_border = (1,3)
                    elif self.direction == DOWN:
                        current_border = (1,6)
                elif set(candidate_borders) == {(1,5), (1,6)}:
                    if self.direction == LEFT:
                        current_border = (1,5)
                    elif self.direction == DOWN:
                        current_border = (1,6)
                elif set(candidate_borders) == {(2,5), (2,4)}:
                    if self.direction == LEFT:
                        current_border = (2,5)
                    elif self.direction == UP:
                        current_border = (2,4)
                elif set(candidate_borders) == {(3,1), (3,6)}:
                    if self.direction == DOWN:
                        current_border = (3,1)
                    elif self.direction == RIGHT:
                        current_border = (3,6)
                elif set(candidate_borders) == {(5,1), (5,2)}:
                    if self.direction == LEFT:
                        current_border = (5,2)
                    elif self.direction == UP:
                        current_border = (5,1)
                elif set(candidate_borders) == {(6,1), (6,3)}:
                    if self.direction == UP:
                        current_border = (6,1)
                    elif self.direction == RIGHT:
                        current_border = (6,3)
                elif set(candidate_borders) == {(6,3), (6,4)}:
                    if self.direction == RIGHT:
                        current_border = (6,3)
                    elif self.direction == DOWN:
                        current_border = (6,4)      
        else:
            current_border = candidate_borders[0]
        
        return current_border

    def next_spot(self):
        next_x = (self.x + self.direction[0]) % self.maze_height
        next_y = (self.y + self.direction[1]) % self.maze_width
        turn = None
        if self.maze[next_x][next_y] == VOID:
            next_x, next_y, turn = self.teleport(next_x, next_y)
        return next_x, next_y, turn

    def step(self):
        next_x, next_y, turn = self.next_spot()
        if self.is_way_forward(next_x, next_y):
            self.x, self.y = next_x, next_y                
            if turn:
                turn()
            return True
        else:
            return False

    def teleport(self, x, y):
        next_x, next_y = x, y
        turn = None

        if self.part == 1:
            while self.maze[next_x][next_y] == VOID:
                next_x = (next_x + self.direction[0]) % self.maze_height
                next_y = (next_y + self.direction[1]) % self.maze_width
        
        elif self.part == 2:
            border = self.get_current_border()
            jumps = self.jump_table[border][0]
            turn = self.jump_table[border][1]
            next_x, next_y = jumps[(self.x, self.y)]

        return next_x, next_y, turn

    def is_way_forward(self, next_x, next_y):
        return self.maze[next_x][next_y] != WALL

    def go(self):
        for move in self.moves:
            if isinstance(move, int):
                for _ in range(move):
                    success = self.step()
                    if not success: 
                        break
            else:
                move()
        
    def calculate_score(self):
        return 1000 * (self.x + 1) + 4 * (self.y + 1) + DIRECTION_SCORE[self.direction]

    def print_maze(self):
        for i, line in enumerate(self.maze):
            if i == self.x:
                line[self.y] = PLAYER_ICON[self.direction]
            print(''.join(line))

test_data = '''        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5'''

print('Testing...')
raw_maze, moves = test_data.split('\n\n')
raw_maze_lines = raw_maze.splitlines()
maze = get_proper_maze(raw_maze_lines)
P = Player(maze, 1)
P.parse_instructions(moves)
P.go()
print('Testing part 1:', P.calculate_score() == 6032)

with open('inp', mode='r') as inp:
    print('Solution...')
    inp_map = inp.read()
    raw_maze, moves = inp_map.split('\n\n')
    raw_maze_lines = raw_maze.splitlines()
    maze = get_proper_maze(raw_maze_lines)
    P = Player(maze, 1)
    P.parse_instructions(moves)
    P.go()
    print('Final score for part 1:', P.calculate_score())
    P = Player(maze, 2)
    P.parse_instructions(moves)
    P.go()
    print('Final score for part 2:', P.calculate_score())
