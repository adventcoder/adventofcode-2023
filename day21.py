import aoc
from collections import Counter

@aoc.command()
@aoc.pass_input()
def step(inp, r=65):
    grid = inp.splitlines()
    ps = start(grid)
    t = 0
    while True:
        ps = step(ps, grid)
        t += 1
        if t % 131 == r:
            print(f'[{t} = {t//131}*131 + {r}]')
            print_counts(ps, grid)
            input()

def print_counts(ps, grid):
    counts = group(ps, grid)
    x0 = min(x for x, _ in counts)
    x1 = max(x for x, _ in counts)
    y0 = min(y for _, y in counts)
    y1 = max(y for _, y in counts)
    for y in range(y0, y1 + 1):
        row = []
        for x in range(x0, x1 + 1):
            row.append('%4d' % counts[(x, y)])
        print(*row)

@aoc.puzzle()
def part1(inp):
    grid = inp.splitlines()
    ps = start(grid)
    for _ in range(64):
        ps = step(ps, grid)
    return group(ps, grid)[(0, 0)]

@aoc.puzzle()
def part2(inp):
    return count(inp.splitlines(), 26501365)

def count(grid, t):
    n, r = divmod(t, 131) # t = 131*n + r
    assert r < 66
    assert n > 0
    # The area looks like this:
    #
    #     x U x
    #   x y a y x
    # x y a b a y x
    # L a b a b a R    n=3
    # x y a b a y x
    #   x y a y x
    #     x D x
    #
    # There are n^2 a's and (n-1)^2 b's in the interior.
    #
    # There are n x's and n-1 y's per diagonal.
    # Not shown here but the values for x,y are all the same per diagonal.
    #
    # All the values for a, b, x, y can be calculated for n=2, t=131*2 + r, and then just multiplied by n.
    #
    ps = start(grid)
    for _ in range(131*2 + r):
        ps = step(ps, grid)
    counts = group(ps, grid)
    # interior
    area = n*n*counts[(1, 0)] + (n-1)*(n-1)*counts[(0, 0)]
    # diagonals
    for x, y in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        area += n*counts[(2*x, y)] + (n-1)*counts[(x, y)]
    # tips
    for x, y in adj((0, 0)):
        area += counts[2*x, 2*y]
    return area

def group(ps, grid):
    return Counter((x // len(grid[0]), y // len(grid)) for x, y in ps)

def start(grid):
    return { (x, y) for y, row in enumerate(grid) for x, c in enumerate(row) if c == 'S' }

def step(ps, grid):
    return { n for p in ps for n in adj(p) if get(n, grid) != '#' }

def get(p, grid):
    x, y = p
    return grid[y % len(grid)][x % len(grid[0])]

def adj(p):
    x, y = p
    yield x + 1, y
    yield x, y + 1
    yield x - 1, y
    yield x, y - 1

if __name__ == '__main__':
    aoc.main()
