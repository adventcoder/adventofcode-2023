import aoc
from collections import deque
from math import lcm

#TODO: cleanup?

@aoc.command()
@aoc.pass_input()
def makedot(inp):
    print('digraph {')
    for line in inp.splitlines():
        name, line = line.split(' -> ')
        if name[0] == '%':
            name = name[1:]
            print(f'    {name} [shape="box"];')
        elif name[0] == '&':
            name = name[1:]
            print(f'    {name} [shape="diamond"];')
        for out in line.split(', '):
            print(f'    {name} -> {out};')
    print('}')

@aoc.puzzle()
def part1(inp):
    modules = parse_modules(inp)
    counts = [0] * 2
    queue = deque()
    for _ in range(1000):
        queue.append(('broadcaster', 0, 'button'))
        while queue:
            name, pulse, input = queue.popleft()
            counts[pulse] += 1
            queue.extend(modules[name].recv(pulse, input))
    return counts[0] * counts[1]

@aoc.puzzle()
def part2(inp):
    modules = parse_modules(inp)
    ends = set(input for name in modules['rx'].inputs for input in modules[name].inputs)
    cycles = [presses(start, ends, modules) for start in modules['broadcaster'].outputs]
    return lcm(*cycles)

def presses(start, ends, modules):
    queue = deque()
    presses = 0
    while True:
        queue.append((start, 0, 'broadcaster'))
        presses += 1
        while queue:
            name, pulse, input = queue.popleft()
            if name in ends and pulse == 0:
                return presses
            queue.extend(modules[name].recv(pulse, input))

def parse_modules(inp):
    modules = {}
    for line in inp.splitlines():
        mod = Module(line)
        modules[mod.name] = mod
    mod = Module('rx')
    modules[mod.name] = mod
    for mod in modules.values():
        for output in mod.outputs:
            modules[output].inputs.append(mod.name)
    return modules

class Module:
    def __init__(self, line):
        name, *rest = line.split(' -> ')
        self.outputs = rest[0].split(', ') if rest else []
        self.inputs = []
        if not name[0].isalpha():
            self.type = name[0]
            self.name = name[1:]
            if self.type == '%':
                self.state = 0
            elif self.type == '&':
                self.state = {}
        else:
            self.type = None
            self.name = name

    def recv(self, pulse, input):
        if self.type == '%':
            if pulse == 1:
                return
            self.state ^= 1
            pulse = self.state
        elif self.type == '&':
            self.state[input] = pulse
            pulse = 0 if all(self.state.get(input, 0) for input in self.inputs) else 1
        for output in self.outputs:
            yield output, pulse, self.name

if __name__ == '__main__':
    aoc.main()
