import aoc
from math import prod

colors = ['red', 'green', 'blue']
max_counts = [12, 13, 14]

@aoc.puzzle()
def part1(inp):
    return sum(id for id, hands in parse_games(inp) if possible(hands))

@aoc.puzzle()
def part2(inp):
    return sum(prod(min_counts(hands)) for _, hands in parse_games(inp))

def parse_games(inp):
    for line in inp.splitlines():
        label, rest = line.split(':')
        id = int(label.split()[-1])
        yield id, parse_hands(rest)

def parse_hands(s):
    for chunk in s.split(';'):
        yield parse_hand(chunk)

def parse_hand(s):
    tokens = s.replace(',', '').split()
    for i in range(0, len(tokens), 2):
        yield int(tokens[i]), colors.index(tokens[i + 1])

def possible(hands):
    return all(n <= max_counts[color] for hand in hands for n, color in hand)

def min_counts(hands):
    counts = [0, 0, 0]
    for hand in hands:
        for n, color in hand:
            if n > counts[color]:
                counts[color] = n
    return counts

if __name__ == '__main__':
    aoc.main()
