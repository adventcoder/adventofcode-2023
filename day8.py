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
    lattice = Lattice()
    steps = 0
    for name in nodes:
        if name.endswith('A'):
            end_offsets, loop_offset, period = solve_steps(name, dirs, nodes)
            assert len(end_offsets) == 1
            end_offset = end_offsets[0]
            assert end_offset >= loop_offset
            lattice &= Lattice(end_offset, period)
            steps += (lattice.start - max(steps, end_offset)) % lattice.step # ceil steps to fit lattice
    return steps

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
    prev_steps = {}
    end_steps = []
    while True:
        for i, d in enumerate(dirs):
            key = (pos, i)
            if key in prev_steps:
                return end_steps, prev_steps[key], steps - prev_steps[key]
            prev_steps[key] = steps
            if pos.endswith('Z'):
                end_steps.append(steps)
            pos = nodes[pos][d]
            steps += 1

if __name__ == '__main__':
    aoc.main()
