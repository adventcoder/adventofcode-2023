import aoc
from math import prod

colors = ['red', 'green', 'blue']
max_counts = [12, 13, 14]

@aoc.puzzle()
def part1(games):
    return sum(id for id, hands in parse_games(games) if possible(hands))

@aoc.puzzle()
def part2(games):
    return sum(prod(min_counts(hands)) for _, hands in parse_games(games))

def parse_games(inp):
    for line in inp.splitlines():
        label, hands = line.split(':')
        id = int(label.split()[-1])
        yield id, hands

def parse_hand(hand):
    tokens = hand.replace(',', '').split()
    for i in range(0, len(tokens), 2):
        yield int(tokens[i]), colors.index(tokens[i + 1])

def possible(hands):
    for hand in hands.split(';'):
        for n, color in parse_hand(hand):
            if n > max_counts[color]:
                return False
    return True

def min_counts(hands):
    counts = [0, 0, 0]
    for hand in hands.split(';'):
        for n, color in parse_hand(hand):
            if n > counts[color]:
                counts[color] = n
    return counts

if __name__ == '__main__':
    aoc.main()
