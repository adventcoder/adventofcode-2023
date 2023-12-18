import aoc

E = 0
S = 1
W = 2
N = 3

dx = [1, 0, -1,  0]
dy = [0, 1,  0, -1]

dirs = {
    '|': (N, S),
    '-': (E, W),
    'L': (N, E),
    'J': (N, W),
    '7': (S, W),
    'F': (S, E),
}

def reverse(d):
    return (d + 2) % 4

def apply(c, d):
    d1, d2 = dirs[c]
    return d1 + d2 - reverse(d)

def start(grid):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == 'S':
                return x, y, start_dir(grid, x, y)

def start_dir(grid, x, y):
    for d in range(4):
        nx = x + dx[d]
        ny = y + dy[d]
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]) and reverse(d) in dirs[grid[ny][nx]]:
            return d

@aoc.puzzle()
def part1(inp):
    grid = inp.splitlines()
    x, y, d = start(grid)
    n = 0
    while True:
        x += dx[d]
        y += dy[d]
        n += 1
        if grid[y][x] == 'S':
            break
        d = apply(grid[y][x], d)
    return n // 2

@aoc.puzzle()
def part2(inp):
    grid = inp.splitlines()
    x, y, d = start(grid)
    area = 0
    edge = 0
    while True:
        px, x = x, x + dx[d]
        py, y = y, y + dy[d]
        area += px*y - x*py
        edge += 1
        if grid[y][x] == 'S':
            break
        d = apply(grid[y][x], d)
    return (abs(area) - edge)//2 + 1

if __name__ == '__main__':
    aoc.main()
