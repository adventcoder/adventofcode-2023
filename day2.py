import aoc
from math import prod

max_counts = { 'red': 12, 'green': 13, 'blue': 14}

@aoc.puzzle()
def part1(inp):
    return sum(id for id, hands in parse_games(inp) if all(possible(hand) for hand in hands))

@aoc.puzzle()
def part2(inp):
    return sum(prod(min_counts(hands).values()) for _, hands in parse_games(inp))

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
        yield int(tokens[i]), tokens[i + 1]

def possible(hand):
    return all(n <= max_counts[color] for n, color in hand)

def min_counts(hands):
    counts = { 'red': 0, 'green': 0, 'blue': 0}
    for hand in hands:
        for n, color in hand:
            if n > counts[color]:
                counts[color] = n
    return counts

if __name__ == '__main__':
    aoc.main()
