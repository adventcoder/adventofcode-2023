import aoc

#TODO: rewrite to shoelace formula

#   3
# 1 + 2
#   0
dx = [0, -1, 1,  0]
dy = [1,  0, 0, -1]

dirs = {
    '7': (0, 1),
    'F': (0, 2),
    '|': (0, 3),
    '-': (1, 2),
    'J': (1, 3),
    'L': (2, 3)
}

def move(x, y, d):
    return x + dx[d], y + dy[d]

def turn(d, c):
    d0, d1 = dirs[c]
    return d + d0 + d1 - 3

def connects(grid, x, y, d):
    nx = x + dx[d]
    ny = y + dy[d]
    return 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]) and 3 - d in dirs[grid[ny][nx]]

@aoc.puzzle()
def part1(inp):
    grid = inp.splitlines()
    Sx, Sy = next((x, y) for y, line in enumerate(grid) for x, c in enumerate(line) if c == 'S')
    d = next(d for d in range(4) if connects(grid, Sx, Sy, d))
    x, y = move(Sx, Sy, d)
    n = 1
    while x != Sx or y != Sy:
        d = turn(d, grid[y][x])
        x, y = move(x, y, d)
        n += 1
    return n // 2

@aoc.puzzle()
def part2_old(inp):
    grid = inp.splitlines()
    loop = [[False] * len(line) for line in grid]
    Sx, Sy = next((x, y) for y, line in enumerate(grid) for x, c in enumerate(line) if c == 'S')
    c = next(c for c in dirs.keys() if all(connects(grid, Sx, Sy, d) for d in dirs[c]))
    grid[Sy] = grid[Sy][:Sx] + c + grid[Sy][Sx+1:]
    loop[Sy][Sx] = True
    d = dirs[c][0]
    x, y = move(Sx, Sy, d)
    while x != Sx or y != Sy:
        loop[y][x] = True
        d = turn(d, grid[y][x])
        x, y = move(x, y, d)
    area = 0
    for y, row in enumerate(grid):
        inside = 0
        x = 0
        while x < len(row):
            c = row[x]
            if loop[y][x]:
                if c == '|':
                    inside ^= 1
                else:
                    assert c in 'LF'
                    x += 1
                    while row[x] == '-':
                        x += 1
                    if (c == 'F' and row[x] == 'J') or (c == 'L' and row[x] == '7'):
                        inside ^= 1
            else:
                area += inside
            x += 1
    return area

if __name__ == '__main__':
    aoc.main()
