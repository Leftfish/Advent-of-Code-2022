from enum import IntEnum

print('Day 2 of Advent of Code!')

class Play(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    
    @property
    def beats(self):
        rules = {Play.ROCK: Play.SCISSORS, Play.SCISSORS: Play.PAPER, Play.PAPER: Play.ROCK}
        return rules[self]

    @property
    def loses_to(self):
        rules = {Play.SCISSORS: Play.ROCK, Play.PAPER: Play.SCISSORS, Play.ROCK: Play.PAPER}
        return rules[self]

class Result(IntEnum):
    LOSE = 0
    DRAW = 3
    WIN = 6

PLAYS = {'A': Play.ROCK, 'X': Play.ROCK, 'B': Play.PAPER, 'Y': Play.PAPER, 'C': Play.SCISSORS, 'Z': Play.SCISSORS} 
SECRET_PLAYS = {'A': Play.ROCK, 'B': Play.PAPER, 'C': Play.SCISSORS, 'X': Result.LOSE, 'Y': Result.DRAW, 'Z': Result.WIN}

def parse_rounds(raw_rounds):
    return [play.split() for play in raw_rounds]

def score_part1(opponent_shape, player_shape): 
    if player_shape.beats == opponent_shape:
        return player_shape + Result.WIN
    elif opponent_shape.beats == player_shape:
        return player_shape + Result.LOSE
    else:
        return player_shape + Result.DRAW

def score_part2(opponent_shape, player_strategy):
    if player_strategy == Result.WIN:
        return player_strategy + opponent_shape.loses_to
    elif player_strategy == Result.LOSE:
        return player_strategy + opponent_shape.beats
    elif player_strategy == Result.DRAW:
        return player_strategy + opponent_shape

def play_all(rounds, playbook, score_calculator):
    def single_round(pair_of_plays):
        return (playbook[pair_of_plays[0]], playbook[pair_of_plays[1]])
    
    return sum(score_calculator(*single_round(pair_of_plays)) for pair_of_plays in rounds)

test_data = '''A Y
B X
C Z'''

print('Testing...')
rounds = parse_rounds(test_data.splitlines())
print('Normal rules:', play_all(rounds, PLAYS, score_part1) == 15)
print('Weird secret rules:', play_all(rounds, SECRET_PLAYS, score_part2) == 12)

print('Solution...')
with open('inp.dat', mode='r') as inp:
    rounds = parse_rounds(inp.readlines())
    print('Normal rules:', play_all(rounds, PLAYS, score_part1))
    print('Weird secret rules:', play_all(rounds,  SECRET_PLAYS, score_part2))