import aoc
from collections import Counter

@aoc.puzzle()
def part1(inp):
    return energy(inp.split(), 0, 0, 1, 0)

@aoc.puzzle()
def part2(inp):
    #TODO: very slow
    grid = inp.split()
    return max(energy(grid, *beam) for beam in beams(grid))

def beams(grid):
    w = len(grid[0])
    h = len(grid)
    for x in range(w):
        yield x, 0, 0, 1
        yield x, h - 1, 0, -1
    for y in range(h):
        w = len(grid[y])
        yield 0, y, 0, 1
        yield w - 1, y, 0, -1

def energy(grid, x, y, dx, dy):
    stack = [(x, y, dx, dy)]
    seen = set()
    energy = Counter()
    while stack:
        x, y, dx, dy = stack.pop()
        while 0 <= y < len(grid) and 0 <= x < len(grid[y]) and (x, y, dx, dy) not in seen:
            seen.add((x, y, dx, dy))
            energy[(x, y)] += 1
            c = grid[y][x]
            if c == '/':
                dx, dy = -dy, -dx
            elif c == '\\':
                dx, dy = dy, dx
            elif c == '|':
                if dy == 0:
                    stack.append((x, y - 1, 0, -1))
                    dx, dy = 0, 1
            elif c == '-':
                if dx == 0:
                    stack.append((x - 1, y, -1, 0))
                    dx, dy = 1, 0
            else:
                assert c == '.'
            x += dx
            y += dy
    return len(energy)

if __name__ == '__main__':
    aoc.main()
