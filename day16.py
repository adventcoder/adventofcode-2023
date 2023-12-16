import aoc

@aoc.puzzle()
def part1(inp):
    return energy(inp.split(), (0, 0, 1, 0))

#TODO: very slow
@aoc.puzzle()
def part2(inp):
    grid = inp.split()
    return max(energy(grid, start) for start in starts(grid))

def starts(grid):
    for x in range(len(grid[0])):
        yield x, 0, 0, 1
        yield x, len(grid) - 1, 0, -1
    for y in range(len(grid)):
        yield 0, y, 0, 1
        yield len(grid[y]) - 1, y, 0, -1

def neighbours(pos, grid):
    x, y, dx, dy = pos
    for ndx, ndy in reflect(dx, dy, grid[y][x]):
        nx = x + ndx
        ny = y + ndy
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]):
            yield nx, ny, ndx, ndy

def reflect(dx, dy, c):
    if c == '/':
        yield -dy, -dx
    elif c == '\\':
        yield dy, dx
    elif c == '|' and dy == 0:
        yield 0, -dx
        yield 0,  dx
    elif c == '-' and dx == 0:
        yield -dy, 0
        yield  dy, 0
    else:
        assert c == '.' or (c == '|' and dx == 0) or (c == '-' and dy == 0)
        yield dx, dy

def energy(grid, start):
    stack = [start]
    seen = set([start])
    while stack:
        pos = stack.pop()
        for n in neighbours(pos, grid):
            if n not in seen:
                stack.append(n)
                seen.add(n)
    return len(set((x, y) for x, y, _, _ in seen))

if __name__ == '__main__':
    aoc.main()
