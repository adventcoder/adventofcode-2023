import aoc
from collections import deque, defaultdict
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
    inputs, outputs, groups = parse_modules(inp)
    counts = [0] * 2
    # We only need to keep track of the last output pulse for each module
    pulses = { name: 0 for name in outputs }
    queue = deque()
    for _ in range(1000):
        counts[0] += 1
        queue.extend(('broadcaster', output) for output in outputs['broadcaster'])
        while queue:
            input, name = queue.popleft()
            counts[pulses[input]] += 1
            if name in groups['%']:
                if pulses[input] == 0:
                    pulses[name] ^= 1
                    queue.extend((name, output) for output in outputs[name])
            elif name in groups['&']:
                pulses[name] = 0 if all(pulses[input] for input in inputs[name]) else 1
                queue.extend((name, output) for output in outputs[name])
    return counts[0] * counts[1]

@aoc.puzzle()
def part2(inp):
    _, outputs, groups = parse_modules(inp)
    cycles = [cycle_time(start, outputs, groups) for start in outputs['broadcaster']]
    return lcm(*cycles)

def cycle_time(start, outputs, groups):
    common, = set(outputs[start]) & groups['&']
    n = 0
    shift = 0
    while True:
        if common in outputs[start]:
            n |= 1 << shift
        shift += 1
        nexts = set(outputs[start]) & groups['%'] 
        if not nexts:
            break
        start, = nexts
    return n

def parse_modules(inp):
    inputs = {}
    outputs = {}
    groups = defaultdict(set)
    for line in inp.splitlines():
        name, line = line.split(' -> ')
        if not name[0].isalpha():
            groups[name[0]].add(name[1:])
            name = name[1:]
        inputs[name] = []
        outputs[name] = line.split(', ')
    inputs['rx'] = []
    for name in outputs:
        for output in outputs[name]:
            inputs[output].append(name)
    return inputs, outputs, groups

if __name__ == '__main__':
    aoc.main()
