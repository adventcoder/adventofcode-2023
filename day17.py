import aoc
from collections import defaultdict

@aoc.puzzle()
def part1(inp):
    grid = parse_grid(inp)
    def moves(pos):
        x, y, dx, dy, n = pos
        if n < 3:
            yield x + dx, y + dy, dx, dy, n + 1
        yield x - dy, y + dx, -dy, dx, 1
        yield x + dy, y - dx, dy, -dx, 1
    def goal(pos):
        x, y, _, _, _ = pos
        return y == len(grid) - 1 and x == len(grid[y]) - 1
    return find_path(grid, moves, (0, 0, 1, 0, 0), goal)

@aoc.puzzle()
def part2(inp):
    grid = parse_grid(inp)
    def moves(pos):
        x, y, dx, dy, n = pos
        if n < 10:
            yield x + dx, y + dy, dx, dy, n + 1
        if n >= 4:
            yield x - dy, y + dx, -dy, dx, 1
            yield x + dy, y - dx, dy, -dx, 1
    def goal(pos):
        x, y, _, _, n = pos
        return y == len(grid) - 1 and x == len(grid[y]) - 1 and n >= 4
    return find_path(grid, moves, (0, 0, 1, 0, 0), goal)

def parse_grid(inp):
    return [[int(c) for c in line] for line in inp.splitlines()]

def find_path(grid, moves, start, goal):
    loss = { start: 0 }
    q = defaultdict(set)
    push(q, 0, start)
    while q:
        assert len(q) <= 10 # since heat loss values are single digits
        p = pop(q, min(q))
        if goal(p):
            return loss[p]
        for n in moves(p):
            if valid(n[0], n[1], grid):
                new_loss = loss[p] + grid[n[1]][n[0]]
                if n not in loss:
                    loss[n] = new_loss
                    push(q, new_loss, n)
                elif new_loss < (old_loss := loss[n]):
                    loss[n] = new_loss
                    pop(q, old_loss, n)
                    push(q, new_loss, n)

def push(q, k, v):
    q[k].add(v)

def pop(q, k, v=None):
    if v is None:
        v = q[k].pop()
    else:
        q[k].pop(v)
    if not q[k]:
        del q[k]
    return v

def valid(x, y, grid):
    return 0 <= y < len(grid) and 0 <= x < len(grid[y])

if __name__ == '__main__':
    aoc.main()
