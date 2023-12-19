import aoc

colors = ('red', 'green', 'blue')

@aoc.puzzle()
def part1(inp):
    ans = 0
    for line in inp.splitlines():
        label, game = line.split(': ')
        r, g, b = min_counts(game)
        if r <= 12 and g <= 13 and b <= 14:
            ans += int(label.split()[-1])
    return ans

@aoc.puzzle()
def part2(inp):
    ans = 0
    for line in inp.splitlines():
        r, g, b = min_counts(line.split(': ')[1])
        ans += r * g * b
    return ans

def min_counts(game):
    counts = [0] * len(colors)
    for hand in game.split('; '):
        for entry in hand.split(', '):
            pair = entry.split()
            n = int(pair[0])
            i = colors.index(pair[1])
            counts[i] = max(counts[i], n)
    return counts

if __name__ == '__main__':
    aoc.main()
