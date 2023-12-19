import aoc
from math import prod

@aoc.puzzle()
def part1(inp):
    chunks = inp.split('\n\n')
    workflows = parse_workflows(chunks[0])
    parts = parse_parts(chunks[1])
    return sum(value for part in parts if accepted(workflows, part) for value in part.values())

@aoc.puzzle()
def part2(inp):
    chunks = inp.split('\n\n')
    workflows = parse_workflows(chunks[0])
    parts = { c: range(1, 4001) for c in 'xmas' }
    return count_accepted(workflows, parts)

def parse_workflows(chunk):
    workflows = {}
    for line in chunk.splitlines():
        i = line.index('{')
        workflows[line[:i]] = Workflow(line[i+1:-1].split(','))
    return workflows

def parse_parts(chunk):
    for line in chunk.splitlines():
        part = {}
        for expr in line[1:-1].split(','):
            name, value = expr.split('=')
            part[name] = int(value)
        yield part

def accepted(workflows, part, name='in'):
    while True:
        if name == 'R':
            return False
        if name == 'A':
            return True
        name = workflows[name].apply(part)

def count_accepted(workflows, parts, name='in'):
    if name == 'R':
        return 0
    if name == 'A':
        return prod(len(values) for values in parts.values())
    total = 0
    for expr, target in workflows[name].rules:
        total += count_accepted(workflows, expr.filter(parts), target)
        parts = expr.filter_complement(parts)
    total += count_accepted(workflows, parts, workflows[name].default_target)
    return total

class Workflow:
    def __init__(self, rules):
        self.default_target = rules.pop()
        self.rules = []
        for rule in rules:
            expr, target = rule.split(':')
            self.rules.append((Expr(expr), target))

    def apply(self, part):
        for expr, target in self.rules:
            if expr.test(part):
                return target
        return self.default_target

class Expr:
    def __init__(self, expr):
        self.name = expr[0]
        self.op = expr[1]
        self.value = int(expr[2:])

    def test(self, part):
        if self.op == '<':
            return part[self.name] < self.value
        if self.op == '>':
            return part[self.name] > self.value

    def filter(self, parts):
        values = parts[self.name]
        if self.op == '<': # values & range(-inf, self.value)
            return { **parts, self.name: range(values.start, min(values.stop, self.value)) }
        if self.op == '>': # values & range(self.value + 1, inf)
            return { **parts, self.name: range(max(values.start, self.value + 1), values.stop) }

    def filter_complement(self, parts):
        values = parts[self.name]
        if self.op == '<': # values & range(self.value, inf)
            return { **parts, self.name: range(max(values.start, self.value), values.stop) }
        if self.op == '>': # values & range(-inf, self.value + 1)
            return { **parts, self.name: range(values.start, min(values.stop, self.value + 1)) }

if __name__ == '__main__':
    aoc.main()
