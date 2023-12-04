import aoc

@aoc.puzzle()
def part1(inp):
    ans = 0
    for card in inp.splitlines():
        matches = find_matches(card)
        if matches > 0:
            ans += 2**(matches - 1)
    return ans

@aoc.puzzle()
def part2(inp):
    cards = inp.splitlines()
    copies = [1] * len(cards)
    for i, card in enumerate(cards):
        for j in range(find_matches(card)):
            copies[i + j + 1] += copies[i]
    return sum(copies)

def find_matches(card):
    lhs, rhs = card.split(':', 2)[1].split('|')
    winning_nums = set(int(s) for s in lhs.split())
    return sum(int(s) in winning_nums for s in rhs.split())

if __name__ == '__main__':
    aoc.main()
