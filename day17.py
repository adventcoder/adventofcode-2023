import aoc
from collections import deque

dx = [1, 0, -1,  0]
dy = [0, 1,  0, -1]

@aoc.puzzle()
def part1(inp):
    grid = parse_grid(inp)
    def moves(pos):
        x, y, d, n = pos
        if n < 3:
            yield move(x, y, d, n)
        yield move(x, y, (d - 1) % 4, 0)
        yield move(x, y, (d + 1) % 4, 0)
    def goal(pos):
        x, y, _, _ = pos
        return y == len(grid) - 1 and x == len(grid[y]) - 1
    return find_path(grid, moves, (0, 0, 0, 0), goal)

@aoc.puzzle()
def part2(inp):
    grid = parse_grid(inp)
    def moves(pos):
        x, y, d, n = pos
        if n < 10:
            yield move(x, y, d, n)
        if n >= 4:
            yield move(x, y, (d - 1) % 4, 0)
            yield move(x, y, (d + 1) % 4, 0)
    def goal(pos):
        x, y, _, n = pos
        return y == len(grid) - 1 and x == len(grid[y]) - 1 and n >= 4
    return find_path(grid, moves, (0, 0, 0, 0), goal)

def parse_grid(inp):
    return [[int(c) for c in line] for line in inp.splitlines()]

def move(x, y, d, n):
    return x + dx[d], y + dy[d], d, n + 1

def find_path(grid, moves, start, goal):
    loss = { start: 0}
    q = deque(set() for _ in range(9))
    q[0].add(start)
    while True:
        q.append(set())
        for p in q[0]:
            if goal(p):
                return loss[p]
            for n in moves(p):
                if valid(n[0], n[1], grid):
                    new_loss = loss[p] + grid[n[1]][n[0]]
                    old_loss = loss.get(n)
                    if old_loss is None or new_loss < old_loss:
                        loss[n] = new_loss
                        if old_loss is not None:
                            q[old_loss - loss[p]].remove(n)
                        q[new_loss - loss[p]].add(n)
        q.popleft()

def valid(x, y, grid):
    return 0 <= y < len(grid) and 0 <= x < len(grid[y])

if __name__ == '__main__':
    aoc.main()
