import aoc
from collections import Counter

@aoc.puzzle()
def part1(inp):
    return winnings(inp)

@aoc.puzzle()
def part2(inp):
    return winnings(inp.replace('J', '?'))

def winnings(inp):
    pairs = [line.split() for line in inp.splitlines()]
    pairs.sort(key=lambda pair: strength(pair[0]))
    return sum((i+1)*int(pair[1]) for i, pair in enumerate(pairs))

def strength(hand):
    return (type(hand), values(hand))

def type(hand):
    hist = Counter(hand)
    wild = hist.pop('?') if len(hist) > 1 and '?' in hist else 0
    counts = sorted(hist.values(), reverse=True)
    counts[0] += wild
    return counts

def values(hand):
    return ['?23456789TJQKA'.index(c) for c in hand]

if __name__ == '__main__':
    aoc.main()
