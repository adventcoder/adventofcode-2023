import aoc
import re
from math import lcm

#TODO: cleanup

@aoc.puzzle()
def part1(inp):
    return Map(inp).steps('AAA', lambda pos: pos == 'ZZZ')

@aoc.puzzle()
def part2(inp):
    map = Map(inp)
    sizes = []
    for start in map.findall(lambda pos: pos.endswith('A')):
        offsets, start, size = map.steps_full(start, lambda pos: pos.endswith('Z'))
        assert len(offsets) == 1 and offsets[0] >= start and offsets[0] == size
        sizes.append(size)
    return lcm(*sizes)

class Map:
    def __init__(self, inp):
        self.dirs, chunk = inp.split('\n\n')
        self.nodes = {}
        for line in chunk.splitlines():
            name, *subnames = re.findall('\w+', line)
            self.nodes[name] = subnames

    def findall(self, pred):
        return filter(pred, self.nodes)

    def steps(self, start, isend):
        pos = start
        steps = 0
        while True:
            for dir in self.dirs:
                if isend(pos):
                    return steps
                pos = self.step(pos, dir)
                steps += 1

    def steps_full(self, start, isend):
        pos = start
        steps = 0
        seen = {}
        offsets = []
        while True:
            for i, dir in enumerate(self.dirs):
                state = (pos, i)
                if state in seen:
                    return offsets, seen[state], steps - seen[state]
                seen[state] = steps
                if isend(pos):
                    offsets.append(steps)
                pos = self.step(pos, dir)
                steps += 1

    def step(self, pos, dir):
        return self.nodes[pos]['LR'.index(dir)]

if __name__ == '__main__':
    aoc.main()
