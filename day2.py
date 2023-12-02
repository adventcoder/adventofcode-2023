import aoc
from math import prod

colors = ['red', 'green', 'blue']

@aoc.puzzle()
def part1(inp):
    return sum(id for id, hands in parse_games(inp) if all(possible(hand) for hand in hands))

@aoc.puzzle()
def part2(inp):
    return sum(prod(max_hand(hands)) for _, hands in parse_games(inp))

def parse_games(inp):
    for line in inp.splitlines():
        label, body = line.split(':')
        id = int(label.split()[1])
        hands = []
        for chunk in body.split(';'):
            hand = [0] * 3
            tokens = chunk.replace(',', '').split()
            for i in range(0, len(tokens), 2):
                hand[colors.index(tokens[i + 1])] = int(tokens[i])
            hands.append(hand)
        yield id, hands

def possible(hand):
    return hand[0] <= 12 and hand[1] <= 13 and hand[2] <= 14

def max_hand(hands):
    return [max(hand[i] for hand in hands) for i in range(3)]

if __name__ == '__main__':
    aoc.main()
