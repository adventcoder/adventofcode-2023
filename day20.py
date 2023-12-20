import aoc
from collections import deque
from math import lcm

#TODO: this is still ugly

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
        queue.append(('broadcaster', 'button', 0))
        while queue:
            name, input, pulse = queue.popleft()
            counts[pulse] += 1
            queue.extend(modules[name].apply(name, input, pulse))
    return counts[0] * counts[1]

@aoc.puzzle()
def part2(inp):
    modules = parse_modules(inp)
    starts = modules['broadcaster'].outputs
    ends = set()
    for input in modules['rx'].inputs:
        for name in modules[input].inputs:
            ends.add(name)
    cycles = [presses(modules, start, ends) for start in starts]
    return lcm(*cycles)

def presses(modules, start, ends):
    presses = 0
    queue = deque()
    while True:
        presses += 1
        queue.append((start, 'broadcaster', 0))
        while queue:
            name, input, pulse = queue.popleft()
            if name in ends and pulse == 0:
                return presses
            queue.extend(modules[name].apply(name, input, pulse))

def parse_modules(inp):
    modules = {}
    for line in inp.splitlines():
        name, line = line.split(' -> ')
        outputs = line.split(', ')
        type = Broadcaster
        if name[0] == '%':
            name = name[1:]
            type = FlipFlop
        elif name[0] == '&':
            name = name[1:]
            type = Conjunction
        modules[name] = type(outputs)
    modules['rx'] = Broadcaster([])
    for name, module in modules.items():
        for output in module.outputs:
            modules[output].inputs.append(name)
    for module in modules.values():
        module.reset()
    return modules

class Broadcaster:
    def __init__(self, outputs):
        self.outputs = outputs
        self.inputs = []

    def reset(self):
        pass

    def transform(self, input, pulse):
        return pulse

    def apply(self, name, input, pulse):
        pulse = self.transform(input, pulse)
        if pulse is not None:
            for output in self.outputs:
                yield output, name, pulse

class FlipFlop(Broadcaster):
    def reset(self):
        self.state = 0

    def transform(self, input, pulse):
        if pulse == 0:
            self.state ^= 1
            return self.state
        return None

class Conjunction(Broadcaster):
    def reset(self):
        self.state = bytearray(len(self.inputs))

    def transform(self, input, pulse):
        self.state[self.inputs.index(input)] = pulse
        return 0 if all(self.state) else 1

if __name__ == '__main__':
    aoc.main()
