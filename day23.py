import aoc
from collections import defaultdict
from functools import cache
from math import inf
import click

#TODO: super slow and kind of overengineered

slopes = '>v<^'
dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

@aoc.puzzle()
@click.option('--dotfile', type=click.File('w'))
def part1(inp, dotfile):
    grid = inp.splitlines()
    parents = transpose(get_edges(grid))
    if dotfile is not None:
        write_dot(parents, dotfile)

    @cache
    def find_longest_path(curr):
        if is_start(grid, *curr):
            return 0
        return max(find_longest_path(prev) + steps for prev, steps in parents[curr].items())

    return find_longest_path(get_end(grid))

@aoc.puzzle()
@click.option('--dotfile', type=click.File('w'))
def part2(inp, dotfile):
    grid = inp.splitlines()
    edges = get_edges(grid)
    for a, bs in transpose(edges).items():
        for b, steps in bs.items():
            edges[a][b] = steps
    if dotfile is not None:
        write_dot(edges, dotfile)

    def find_longest_path(a, seen):
        if is_end(grid, *a):
            return 0
        # Just dumb bruteforce. We could try eliminate some branches maybe?
        max_steps = -inf
        for b in edges[a]:
            if b in seen:
                continue
            steps = edges[a][b] + find_longest_path(b, seen | frozenset([a]))
            if steps > max_steps:
                max_steps = steps
        return max_steps

    return find_longest_path(get_start(grid), frozenset())

def write_dot(edges, file):
    labels = {}
    for i, a in enumerate(edges):
        labels[a] = str(i)
    print('digraph {', file=file)
    for a in edges:
        for b in edges[a]:
            print(f'{labels[a]} -> {labels[b]} [label={edges[a][b]}]', file=file)
    print('}', file=file)

def transpose(edges):
    new_edges = defaultdict(dict)
    for a in edges:
        for b in edges[a]:
            new_edges[b][a] = edges[a][b]
    return new_edges

def get_edges(grid):
    edges = {}
    edges[get_start(grid)] = dict([get_edge(grid, get_start(grid))])
    edges[get_end(grid)] = {}
    for a in get_junctions(grid):
        edges[a] = {}
        for b in neighbours(grid, *a):
            c, steps = get_edge(grid, b)
            if a != c:
                edges[a][c] = steps + 1
    return edges

def get_edge(grid, curr):
    prev = None
    steps = 0
    while not is_end(grid, *curr) and not is_junction(grid, *curr):
        nexts = [n for n in neighbours(grid, *curr) if n != prev]
        assert len(nexts) == 1
        prev = curr
        curr = nexts[0]
        steps += 1
    return curr, steps

def get_start(grid):
    return (grid[0].index('.'), 0)

def get_end(grid):
    return (grid[-1].index('.'), len(grid) - 1)

def get_junctions(grid):
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[y]) - 1):
            if is_junction(grid, x, y):
                yield x, y

def is_junction(grid, x, y):
    return len(list(neighbours(grid, x, y))) > 2

def is_start(grid, x, y):
    return y == 0

def is_end(grid, x, y):
    return y == len(grid) - 1

def neighbours(grid, x, y):
    c = grid[y][x]
    if c == '.':
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(grid) and grid[ny][nx] != '#':
                yield nx, ny
    elif c in slopes:
        dx, dy = dirs[slopes.index(c)]
        yield x + dx, y + dy

if __name__ == '__main__':
    aoc.main()
