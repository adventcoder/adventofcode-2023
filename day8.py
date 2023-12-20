import aoc
import re
from utils import Lattice

@aoc.puzzle()
def part1(inp):
    dirs, nodes = parse(inp)
    pos = 'AAA'
    steps = 0
    while True:
        for d in dirs:
            if pos == 'ZZZ':
                return steps
            pos = nodes[pos][d]
            steps += 1

@aoc.puzzle()
def part2(inp):
    dirs, nodes = parse(inp)
    ans = Lattice()
    for name in nodes:
        if name.endswith('A'):
            ans &= solve_steps(name, dirs, nodes)
    return ans[1]

def parse(inp):
    chunks = inp.split('\n\n')
    dirs = ['LR'.index(c) for c in chunks[0]]
    nodes = {}
    for line in chunks[1].splitlines():
        names = re.findall('\w+', line)
        nodes[names[0]] = names[1:]
    return dirs, nodes

def solve_steps(pos, dirs, nodes):
    steps = 0
    while not pos.endswith('Z'):
        d = dirs[steps % len(dirs)]
        pos = nodes[pos][d]
        steps += 1
    end = pos
    end_steps = steps
    while True:
        d = dirs[steps % len(dirs)]
        pos = nodes[pos][d]
        steps += 1
        if pos == end:
            return Lattice(end_steps, steps - end_steps)
        assert not pos.endswith('Z') # assume each start has one corresponding end

if __name__ == '__main__':
    aoc.main()
