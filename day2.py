import aoc
from math import prod

max_counts = { 'red': 12, 'green': 13, 'blue': 14 }

@aoc.puzzle()
def part1(inp):
    ans = 0
    for id, hands in map(parse_game, inp.splitlines()):
        if possible(hands):
            ans += id
    return ans

def possible(hands):
    for hand in hands:
        for n, color in hand:
            if n > max_counts[color]:
                return False
    return True

@aoc.puzzle()
def part2(inp):
    ans = 0
    for _, hands in map(parse_game, inp.splitlines()):
        ans += prod(min_counts(hands).values())
    return ans

def min_counts(hands):
    counts = {}
    for hand in hands:
        for n, color in hand:
            if n > counts.get(color, 0):
                counts[color] = n
    return counts

def parse_game(line):
    label, hands = line.split(':', 2)
    id = int(label.split()[-1])
    return id, [parse_hand(hand) for hand in hands.split(';')]

def parse_hand(hand):
    tokens = hand.replace(',', '').split()
    for i in range(0, len(tokens), 2):
        yield int(tokens[i]), tokens[i + 1]

if __name__ == '__main__':
    aoc.main()
