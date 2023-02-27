from collections import deque

print('Day 10 of Advent of Code!')

NOOP = "noop"
ADDX = "addx"

class CPU:
    def __init__(self):
        self.registers = {'X': 1}
        self.instructions = deque()
        self.executing = deque()
        self.cycle = 1
        self.signal_strenghts = {20: None, 60: None, 100: None, 140: None, 180: None, 220: None}
        self.screen = CRT()

    def __repr__(self) -> str:
        return f'CPU cycles: {self.cycle} Register X: {self.registers["X"]}'

    def _parse_instruction(self, line):
        parsed = line.split()
        return (parsed[0], 0) if len(parsed) == 1 else (parsed[0], int(parsed[1]))

    def load_instructions(self, data):
        raw_instructions = data.splitlines()
        for line in raw_instructions:
            name, value = self._parse_instruction(line)
            self.instructions.append(Instruction(name, value))
    
    def _update_signal_strengths(self):
        if self.cycle in self.signal_strenghts:
            self.signal_strenghts[self.cycle] = self.cycle * self.registers['X']

    def _draw_pixel(self):
        position = (self.cycle - 1)
        row = position // self.screen.width
        sprite_position = position - row * self.screen.width
        if sprite_position in self.screen.sprite:
            self.screen.light_pixel(position)

    def _fill_buffer(self):
        if not self.executing and self.instructions:
            self.executing.append(self.instructions.popleft())    

    def execute_next(self):
        self._fill_buffer()
        self._update_signal_strengths()
        self._draw_pixel()

        current = self.executing[0]
        current.cycles -= 1
        self.cycle += 1

        if current.cycles == 0:
            self.registers['X'] += current.value
            self.screen.update_sprite(self.registers['X'])
            self.executing.popleft()     

class CRT:
    def __init__(self, width=40, height=6):
        self.sprite = (0, 1, 2)
        self.width = width
        self.height = height
        self.screen = self.width * self.height * [' ']

    def display(self):
        for i in range(0, len(self.screen), self.width):
            line = self.screen[i:i+self.width]
            print(''.join(line))
        print()

    def update_sprite(self, register):
        self.sprite = (register -1 , register, register + 1)

    def light_pixel(self, position):
        self.screen[position] = '#'

class Instruction:
    def __init__(self, name, value):
        self.name, self.value = name, value
        if name == NOOP:
            self.cycles = 1            
        elif name == ADDX:
            self.cycles = 2

    def __repr__(self) -> str:
        return f'INSTRUCTION: {self.name} cycles: {self.cycles} Value: {self.value}'

test_data = '''addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop'''

print('Testing...')

C = CPU()
C.load_instructions(test_data)
while C.instructions or C.executing:
    C.execute_next()

print('Testing signal strengths...', sum(C.signal_strenghts.values()) == 13140)
print('Testing CRT...')
C.screen.display()

with open('inp.dat', mode='r') as inp:
    print('Solution...')
    test_data = inp.read()
    C = CPU()
    C.load_instructions(test_data)
    while C.instructions or C.executing:
        C.execute_next()
    print('Calculating signal strengths...', sum(C.signal_strenghts.values()))
    print('Displaying image...')
    C.screen.display()
