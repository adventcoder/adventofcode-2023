import aoc
import re
from itertools import cycle
from math import lcm

@aoc.puzzle()
def part1(inp):
    return Map(inp).steps('AAA', lambda name: name == 'ZZZ')

@aoc.puzzle()
def part2(inp):
    map = Map(inp)
    total = 1
    for start in filter(lambda name: name.endswith('A'), map.nodes.keys()):
        total = lcm(total, map.steps(start, lambda name: name.endswith('Z')))
    return total

class Map:
    def __init__(self, inp):
        self.dirs, chunk = inp.split('\n\n')
        self.nodes = {}
        for line in chunk.splitlines():
            name, *subnames = re.findall('\w+', line)
            self.nodes[name] = subnames

    def steps(self, pos, is_end):
        for i, dir in enumerate(cycle(self.dirs)):
            pos = self.nodes[pos]['LR'.index(dir)]
            if is_end(pos):
                return i + 1

if __name__ == '__main__':
    aoc.main()
