import aoc
from collections import defaultdict
from functools import cache
from math import inf

dirs = {
    '>': ( 1,  0),
    'v': ( 0,  1),
    '<': (-1,  0),
    '^': ( 0, -1)
}

@aoc.puzzle()
def part1(inp):
    return find_longest_path(inp.splitlines())

@aoc.puzzle()
def part2(inp):
    for c in dirs.keys():
        inp = inp.replace(c, '.')
    return find_longest_path(inp.splitlines())

def find_longest_path(grid):
    nodes, edges = make_graph(grid)
    @cache
    def recur(i, seen):
        if i == len(nodes) - 1:
            return 0
        max_steps = -inf
        for j in edges[i]:
            if seen & (1 << j):
                continue
            steps = edges[i][j] + recur(j, seen | (1 << i))
            if steps > max_steps:
                max_steps = steps
        return max_steps
    return recur(0, 0)

def make_graph(grid):
    nodes = []
    for y in range(len(grid)):
        for x in range(1, len(grid[y]) - 1):
            if grid[y][x] == '.' and degree(grid, x, y) != 2:
                nodes.append((x, y))
    edges = defaultdict(dict)
    for i, start in enumerate(nodes[:-1]):
        for curr in neighbours(grid, *start):
            prev = start
            steps = 1
            while curr not in nodes:
                nexts = [n for n in neighbours(grid, *curr) if n != prev]
                assert len(nexts) == 1
                prev = curr
                curr = nexts[0]
                steps += 1
            edges[i][nodes.index(curr)] = steps
    return nodes, edges

def degree(grid, x, y):
    count = 0
    for dx, dy in dirs.values():
        nx = x + dx
        ny = y + dy
        if 0 <= ny < len(grid) and (grid[ny][nx] == '.' or grid[ny][nx] in dirs):
            count += 1
    return count

def neighbours(grid, x, y):
    for c, (dx, dy) in dirs.items():
        nx = x + dx
        ny = y + dy
        if 0 <= ny < len(grid) and grid[ny][nx] in ('.', c):
            yield nx, ny

if __name__ == '__main__':
    aoc.main()
