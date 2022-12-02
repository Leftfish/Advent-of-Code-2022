print('Day 2 of Advent of Code!')

ROCK, PAPER, SCISSORS = 1, 2, 3
LOSE, DRAW, WIN = 0, 3, 6

RULES = {ROCK: PAPER, PAPER: SCISSORS, SCISSORS: ROCK}
REVERSE_RULES = {v: k for k, v in RULES.items()}

PLAYS = {'A': ROCK, 'X': ROCK, 'B': PAPER, 'Y': PAPER, 'C': SCISSORS, 'Z': SCISSORS}
SECRET_PLAYS = {'A': ROCK, 'B': PAPER, 'C': SCISSORS, 'X': LOSE, 'Y': DRAW, 'Z': WIN}

def parse_rounds(raw_rounds):
    return [play.split() for play in raw_rounds]

def play_round(rnd, playbook, scoring):
    opp, plr = playbook[rnd[0]], playbook[rnd[1]]
    return scoring(opp, plr)

def score_part1(opp, plr):
    score = plr
    if opp == plr:
        score += DRAW
    elif RULES[plr] == opp:
        score += LOSE
    else:
        score += WIN
    return score

def score_part2(opp, plr):
    score = plr
    if plr == LOSE:
        score += REVERSE_RULES[opp]
    elif plr == DRAW:
        score += opp
    elif plr == WIN:
        score += RULES[opp]
    return score

def play_all(rounds, round_rules, playbook, scoring):
    return sum(round_rules(rnd, playbook, scoring) for rnd in rounds)

test_data = '''A Y
B X
C Z'''

print('Testing...')
rounds = parse_rounds(test_data.splitlines())
print('Normal rules:', play_all(rounds, play_round, PLAYS, score_part1) == 15)
print('Weird secret rules:', play_all(rounds, play_round, SECRET_PLAYS, score_part2) == 12)


print('Solution...')
with open('inp', mode='r') as inp:
    rounds = parse_rounds(inp.readlines())
    print('Normal rules:', play_all(rounds, play_round, PLAYS, score_part1))
    print('Weird secret rules:', play_all(rounds, play_round, SECRET_PLAYS, score_part2))