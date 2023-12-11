import aoc
from itertools import combinations

@aoc.puzzle()
def part1(inp):
    return total_distance(inp, 2)

@aoc.puzzle()
def part2(inp):
    return total_distance(inp, 1000000)

def total_distance(inp, factor):
    grid = inp.splitlines()
    total = 0
    for rows in (grid, zip(*grid)):
        for (y1, n1), (y2, n2) in combinations(expand(rows, factor), 2):
            total += n1*n2*abs(y2-y1)
    return total

def expand(rows, factor):
    y = 0
    for row in rows:
        n = row.count('#')
        yield y, n
        y += factor**(n==0)

if __name__ == '__main__':
    aoc.main()
