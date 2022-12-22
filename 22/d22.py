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
    def __init__(self, maze):
        self.directions = cycle([RIGHT, DOWN, LEFT, UP])
        self.direction = next(self.directions)
        self.moves = []
        self.maze = maze
        self.maze_width = len(self.maze[0])
        self.maze_height = len(self.maze)
        self.start = self._find_start()
        self.x, self.y = self.start

    def _find_start(self):
        return (0, self.maze[0].index(FREE))

    def _parse_instructions(self, moves):
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

    def next_spot(self):
        next_x = (self.x + self.direction[0]) % self.maze_height
        next_y = (self.y + self.direction[1]) % self.maze_width
        if self.maze[next_x][next_y] == VOID:
            next_x, next_y = self.fly_over_void(next_x, next_y)
        return next_x, next_y

    def step(self):
        next_spot = self.next_spot()
        if self.is_way_forward(next_spot):
            self.x, self.y = next_spot
            return True
        else:
            return False

    def fly_over_void(self, x, y):
        next_x, next_y = x, y
        while self.maze[next_x][next_y] == VOID:
            next_x = (next_x + self.direction[0]) % self.maze_height
            next_y = (next_y + self.direction[1]) % self.maze_width
        return next_x, next_y

    def is_way_forward(self, next_spot):
        next_x, next_y = next_spot
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
P = Player(maze)
P._parse_instructions(moves)
P.go()
print('Final score:', P.calculate_score() == 6032)

with open('inp', mode='r') as inp:
    print('Solution...')
    raw_maze, moves = inp.read().split('\n\n')
    raw_maze_lines = raw_maze.splitlines()
    maze = get_proper_maze(raw_maze_lines)
    P = Player(maze)
    P._parse_instructions(moves)
    P.go()
    print('Final score:', P.calculate_score())