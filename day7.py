import aoc
from collections import Counter
from utils import table

#TODO: cleanup

@aoc.puzzle()
def part1(inp):
    return solve(inp, False)

@aoc.puzzle()
def part2(inp):
    return solve(inp, True)

def solve(inp, wildcard):
    pairs = table(inp, (str, int))
    pairs.sort(key=lambda pair: strength(pair[0], wildcard))
    return sum((i+1)*pair[1] for i, pair in enumerate(pairs))

def strength(hand, wildcard):
    return (type(hand, wildcard), values(hand, wildcard))

def type(hand, wildcard):
    hist = Counter(hand)
    jokers = 0
    if wildcard:
        jokers = hist.pop('J') if 'J' in hist else 0
    if hist:
        counts = sorted(hist.values(), reverse=True)
        counts[0] += jokers
        return counts
    else:
        return [jokers]

def values(hand, wildcard=False):
    if wildcard:
        return values(hand.replace('J', '1'))
    else:
        return [int(c) if c.isdigit() else 10 + 'TJQKA'.index(c) for c in hand]

if __name__ == '__main__':
    aoc.main()
