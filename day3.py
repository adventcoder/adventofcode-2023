import aoc
from math import prod

@aoc.puzzle()
def part1(inp):
    grid = inp.splitlines()
    ans = 0
    for y, line in enumerate(grid):
        x0 = 0
        while x0 < len(line):
            if line[x0].isdigit():
                x1 = find_number_end(line, x0) + 1
                if any(is_symbol(get(grid, nx, ny)) for x in range(x0, x1) for nx, ny in neighbours(x, y)):
                    ans += int(line[x0 : x1])
                x0 = x1
            else:
                x0 += 1
    return ans

@aoc.puzzle()
def part2(inp):
    grid = inp.splitlines()
    ans = 0
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == '*':
                nums = {}
                for nx, ny in neighbours(x, y):
                    if get(grid, nx, ny).isdigit():
                        x0 = find_number_start(grid[ny], nx)
                        x1 = find_number_end(grid[ny], nx) + 1
                        nums[(x0, x1, ny)] = int(grid[ny][x0 : x1])
                if len(nums) == 2:
                    ans += prod(nums.values())
    return ans

def is_symbol(c):
    return c != '.' and not c.isdigit()

def neighbours(x, y):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx != 0 or dy != 0:
                yield x + dx, y + dy

def get(grid, x, y):
    return grid[y][x] if 0 <= y < len(grid) and 0 <= x < len(grid[y]) else '.'

def find_number_start(line, x):
    while x > 0 and line[x - 1].isdigit():
        x -= 1
    return x

def find_number_end(line, x):
    while x + 1 < len(line) and line[x + 1].isdigit():
        x += 1
    return x

if __name__ == '__main__':
    aoc.main()
