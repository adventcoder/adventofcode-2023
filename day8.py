import aoc
import re
from math import lcm

@aoc.puzzle()
def part1(inp):
    nodes, dirs = parse_map(inp)
    state = State(nodes, dirs, 'AAA')
    while state.pos != 'ZZZ':
        state.step()
    return state.steps

@aoc.puzzle()
def part2(inp):
    nodes, dirs = parse_map(inp)
    cycles = find_cycles(nodes, dirs)
    return lcm(*cycles)

def parse_map(inp):
    dirs, chunk = inp.split('\n\n')
    nodes = {}
    for line in chunk.splitlines():
        name, *subnames = re.findall('\w+', line)
        nodes[name] = subnames
    return nodes, dirs

def find_cycles(nodes, dirs):
    cycles = []
    for name in nodes.keys():
        if name.endswith('A'):
            state = State(nodes, dirs, name)
            while not state.pos.endswith('Z'):
                state.step()
            end = state.pos
            offset = state.steps
            state.step()
            while state.pos != end:
                if state.pos.endswith('Z'):
                    raise ValueError('Each start must have only one corresponding end')
                state.step()
            cycle = state.steps - offset
            if offset != cycle:
                raise ValueError('Distance from start to end must be the same as the distance from end to end')
            if cycle % len(dirs) != 0:
                raise ValueError('Distance must be a multiple of the number of directions')
            cycles.append(cycle)
    return cycles

class State:
    def __init__(self, nodes, dirs, start):
        self.nodes = nodes
        self.dirs = dirs
        self.pos = start
        self.steps = 0

    def step(self):
        dir = self.dirs[self.steps % len(self.dirs)]
        self.pos = self.nodes[self.pos]['LR'.index(dir)]
        self.steps += 1

if __name__ == '__main__':
    aoc.main()
