from enum import Enum
from itertools import cycle

print('Day 17 of Advent of Code!')

class Rocks(Enum):
    HORIZONTAL_LINE = [[0,2], [0,3], [0,4], [0,5]]
    VERTICAL_LINE = [[0,2], [-1,2], [-2,2], [-3,2]]
    STAR = [[0,3], [-1,2], [-1,3], [-1,4], [-2,3]]
    SQUARE = [[0,2], [0,3], [-1,2], [-1,3]]
    INVERTED_L = [[0,2], [0,3], [0,4], [-1,4], [-2,4]]

class Directions(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

RIGHT_PART_INDEX = {Rocks.HORIZONTAL_LINE: 3, Rocks.VERTICAL_LINE: 0, Rocks.STAR: 3, Rocks.SQUARE: 1, Rocks.INVERTED_L: 2}
LEFT_PART_INDEX = {Rocks.HORIZONTAL_LINE: 0, Rocks.VERTICAL_LINE: 0, Rocks.STAR: 1, Rocks.SQUARE: 0, Rocks.INVERTED_L: 0}

ROCKS_CYCLE = [Rocks.HORIZONTAL_LINE, Rocks.STAR, Rocks.INVERTED_L, Rocks.VERTICAL_LINE, Rocks.SQUARE]

JETS = {'<': Directions.LEFT, '>': Directions.RIGHT}

class FallingRock:
    def __init__(self, shape, top_unoccupied):
        self.shape = shape
        self.coords = [coord[:] for coord in shape.value]

        offset_up = abs(top_unoccupied) + 3
        
        for coord in self.coords:
            coord[0] -= offset_up

    def __repr__(self):
        return f'{self.shape} at coords {self.coords}'
    
    def move(self, move_direction, occupied_spaces, left_border=0, right_border=6):
        def occupied(candidate_coords, occupied_spaces):
            return any(candidate in occupied_spaces for candidate in candidate_coords)
        def on_border(direction):
            if direction == Directions.RIGHT:
                return self.coords[RIGHT_PART_INDEX[self.shape]][1] >= right_border
            elif direction == Directions.LEFT:
                return self.coords[LEFT_PART_INDEX[self.shape]][1] <= left_border
        
        if move_direction == Directions.RIGHT:
            candidate_coords = [(coord[0], coord[1]+1) for coord in self.coords]
            if occupied(candidate_coords, occupied_spaces) or on_border(move_direction):
                return False
            else:
                for coord in self.coords:
                    coord[1] += 1

        elif move_direction == Directions.LEFT:
            candidate_coords = [(coord[0], coord[1]-1) for coord in self.coords]
            if occupied(candidate_coords, occupied_spaces) or on_border(move_direction):
                return False  
            else:
                for coord in self.coords:
                    coord[1] -= 1
            
        elif move_direction == Directions.DOWN:
            candidate_coords = [(coord[0]+1, coord[1]) for coord in self.coords]
            if occupied(candidate_coords, occupied_spaces):
                return False
            else:
                for coord in self.coords:
                    coord[0] += 1
        
        return True

class ElephantTetris:
    def __init__(self, gas_jets):
        self.occupied_spaces = set((1,i) for i in range(7))
        self.top_unoccupied = self.update_top()
        self.current_rock = None
        self.rock_counter = 0
        self.gas_jets = cycle(gas_jets)
        self.total_gas_jets = len(gas_jets)
        self.rocks_cycle = cycle(ROCKS_CYCLE)
        self.horizontal_moves = 0
        self.moves_to_rocks = {}
        self.dejavus = ''

    def update_top(self):
        return min(i for i, j in self.occupied_spaces) - 1

    def drop_rock(self):
        self.current_rock = FallingRock(next(self.rocks_cycle), self.top_unoccupied)
        self.rock_counter += 1

    def move_rock(self):
        next_jet = next(self.gas_jets)
        horizontal_move = JETS[next_jet]
        
        self.horizontal_moves += 1
        jet_id = self.horizontal_moves % self.total_gas_jets
        #print(jet_id, horizontal_move, jet_id in self.moves_to_rocks)

        if jet_id not in self.moves_to_rocks:
            self.moves_to_rocks[jet_id] = self.current_rock.shape
        elif self.moves_to_rocks[jet_id] == self.current_rock.shape:
            self.dejavus += f'\nDEJA VU {jet_id} {self.current_rock} at {self.rock_counter}. Current height: {abs(self.top_unoccupied)}'
            # this adds to a string that can be saved and visually scanned for repeating patterns...

        pushed_by_jets = self.current_rock.move(horizontal_move, self.occupied_spaces)
        moved_down = self.current_rock.move(Directions.DOWN, self.occupied_spaces)

        #print(f'Pushed {horizontal_move}? {pushed_by_jets}')
        #print(f'Moved down? {moved_down}')
        
        if not moved_down:             
            for coord in self.current_rock.coords:
                self.occupied_spaces.add(tuple(coord))
            self.top_unoccupied = self.update_top()
            self.current_rock = None
            return False
        return True

    def play(self, rounds):
        while self.rock_counter < rounds:
            if not self.current_rock:
                self.drop_rock()
            while True:
                move_done = self.move_rock()
                if not move_done:
                    break
        

jets = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

print('Testing...')
g = ElephantTetris(jets)
g.play(2022)
print('Tower after 2022 rounds:', abs(g.top_unoccupied) == 3068)

with open('inp.dat', mode='r') as inp:
    print('Solution...')
    data = inp.read()
    real_game = ElephantTetris(data)
    real_game.play(2022)
    print('Tower after 2022 rounds:', abs(real_game.top_unoccupied))

print('Part 2 solved manually by tracking when rocks and jets start to repeat themselves and then calculating the value thanks to a repeating pattern.')
