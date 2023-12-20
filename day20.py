import aoc
from collections import defaultdict, deque
from math import lcm

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
    gates, outputs, _ = parse_gates(inp)
    counts = [0] * 2
    queue = deque()
    for _ in range(1000):
        queue.append(('button', 'broadcaster', 0))
        while queue:
            from_addr, to_addr, pulse = queue.popleft()
            counts[pulse] += 1
            if to_addr in gates:
                new_pulse = gates[to_addr](from_addr, pulse)
                if new_pulse is not None:
                    for output in outputs[to_addr]:
                        queue.append((to_addr, output, new_pulse))
    return counts[0] * counts[1]

@aoc.puzzle()
def part2(inp):
    gates, outputs, inputs = parse_gates(inp)
    starts = [name for name in outputs['broadcaster']]
    ends = [name2 for name in inputs['rx'] for name2 in inputs[name]]
    total = 1
    for start in starts:
        queue = deque()
        presses = 0
        done = False
        while not done:
            queue.append(('broadcaster', start, 0))
            while queue:
                from_addr, to_addr, pulse = queue.popleft()
                if from_addr in ends and pulse == 1:
                    done = True
                if to_addr in gates:
                    new_pulse = gates[to_addr](from_addr, pulse)
                    if new_pulse is not None:
                        for output in outputs[to_addr]:
                            queue.append((to_addr, output, new_pulse))
            presses += 1
        total = lcm(total, presses)
    return total

def parse_gates(inp):
    gates = {}
    outputs = {}
    inputs = defaultdict(set)
    for line in inp.splitlines():
        name, line = line.split(' -> ')
        if name[0] == '%':
            name = name[1:]
            gates[name] = flipflop()
        elif name[0] == '&':
            name = name[1:]
            gates[name] = conjunction(inputs[name])
        else:
            gates[name] = broadcast
        outputs[name] = line.split(', ')
        for output in outputs[name]:
            inputs[output].add(name)
    return gates, outputs, inputs

def broadcast(addr, pulse):
    return pulse

def flipflop():
    state = 0
    def func(addr, pulse):
        nonlocal state
        if pulse == 0:
            state ^= 1
            return state
        return None
    return func

def conjunction(inputs):
    state = {}
    def func(addr, pulse):
        state[addr] = pulse
        return 0 if all(state.get(name, 0) for name in inputs) else 1
    return func

if __name__ == '__main__':
    aoc.main()
