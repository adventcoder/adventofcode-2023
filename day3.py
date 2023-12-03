import aoc
from math import prod

@aoc.puzzle()
def part1(inp):
    ans = 0
    grid = inp.splitlines()
    symbols = set(find_symbols(grid))
    for x0, x1, y in find_numbers(grid):
        if any(p in symbols for p in boundary(x0, x1, y)):
            ans += int(grid[y][x0 : x1 + 1])
    return ans

@aoc.puzzle()
def part2(inp):
    ans = 0
    grid = inp.splitlines()
    nums = {}
    for x0, x1, y in find_numbers(grid):
        for x in range(x0, x1 + 1):
            nums[(x, y)] = (x0, x1, y)
    for x, y in find_symbols(grid):
        if grid[y][x] == '*':
            adj = set(nums[p] for p in boundary(x, x, y) if p in nums)
            if len(adj) == 2:
                ans += prod(int(grid[y][x0 : x1 + 1]) for x0, x1, y in adj)
    return ans

def find_symbols(grid):
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if not c.isdigit() and c != '.':
                yield x, y

def find_numbers(grid):
    for y, line in enumerate(grid):
        x = 0
        while x < len(line):
            if line[x].isdigit():
                x0 = x
                while x + 1 < len(line) and line[x + 1].isdigit():
                    x += 1
                yield x0, x, y
            x += 1

def boundary(x0, x1, y):
    yield x0 - 1, y
    yield x1 + 1, y
    for x in range(x0 - 1, x1 + 2):
        yield x, y - 1
        yield x, y + 1

if __name__ == '__main__':
    aoc.main()
