import aoc

#   0
# 1 + 2
#   3
dx = [ 0, -1, 1, 0]
dy = [-1,  0, 0, 1]

dirs = {
    'J': (0, 1),
    'L': (0, 2),
    '|': (0, 3),
    '-': (1, 2),
    '7': (1, 3),
    'F': (2, 3)
}

dd = { c: sum(dirs[c]) - 3 for c in dirs }

def start(grid):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == 'S':
                return x, y, start_dir(grid, x, y)

def start_dir(grid, x, y):
    for d in range(4):
        nx = x + dx[d]
        ny = y + dy[d]
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]) and 3 - d in dirs[grid[ny][nx]]:
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
        d += dd[grid[y][x]]
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
        d += dd[grid[y][x]]
    return (abs(area) - edge)//2 + 1

if __name__ == '__main__':
    aoc.main()
