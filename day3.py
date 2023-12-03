import aoc
from math import prod

@aoc.puzzle()
def part1(inp):
    grid = inp.splitlines()
    ans = 0
    for y, line in enumerate(grid):
        for x0, x1, n in get_numbers(line):
            if any(is_symbol(grid[y][x]) for x, y in boundary(grid, x0, x1, y)):
                ans += n
    return ans

@aoc.puzzle()
def part2(inp):
    grid = inp.splitlines()
    ans = 0
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == '*':
                ns = list(get_adj_numbers(grid, x, y))
                if len(ns) == 2:
                    ans += prod(ns)
    return ans

def is_symbol(c):
    return c != '.' and not c.isdigit()

def get_adj_numbers(grid, x, y):
    #TODO: do this more efficiently without recomputing the whole lines
    y0 = max(y - 1, 0)
    y1 = min(y + 1, len(grid) - 1)
    for y in range(y0, y1 + 1):
        for x0, x1, n in get_numbers(grid[y]):
            if x - 1 <= x1 and x + 1 >= x0:
                yield n

def get_numbers(line):
    x = 0
    while x < len(line):
        if line[x].isdigit():
            x0 = x
            while x + 1 < len(line) and line[x + 1].isdigit():
                x += 1
            yield x0, x, int(line[x0 : x + 1])
        x += 1

def boundary(grid, x0, x1, y):
    if x0 > 0:
        x0 -= 1
        yield x0, y
    if x1 < len(grid[y]) - 1:
        x1 += 1
        yield x1, y
    if y > 0:
        for x in range(x0, x1 + 1):
            yield x, y - 1
    if y < len(grid) - 1:
        for x in range(x0, x1 + 1):
            yield x, y + 1

if __name__ == '__main__':
    aoc.main()
