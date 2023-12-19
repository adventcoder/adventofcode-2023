import aoc
from math import prod

#TODO: cleanup?

@aoc.puzzle()
def part1(inp):
    chunks = inp.split('\n\n')
    workflows = parse_workflows(chunks[0])
    return sum(sum(part.values()) for part in parse_parts(chunks[1]) if accepted(workflows, part))

@aoc.puzzle()
def part2(inp):
    chunks = inp.split('\n\n')
    workflows = parse_workflows(chunks[0])
    accepted = accepted_super(workflows, { c: range(1, 4001) for c in 'xmas'})
    return sum(parts(superpart) for superpart in accepted)

def parts(superpart):
    return prod(value.stop - value.start for value in superpart.values())

def parse_workflows(chunk):
    workflows = {}
    for line in chunk.splitlines():
        i = line.index('{')
        rules = []
        for atom in line[i+1:-1].split(','):
            pair = atom.split(':')
            if len(pair) == 1:
                rules.append((pair[0], None))
            else:
                rules.append((pair[1], parse_expr(pair[0])))
        name = line[:i]
        workflows[name] = rules
    return workflows

def parse_parts(chunk):
    for line in chunk.splitlines():
        part = {}
        for atom in line[1:-1].split(','):
            name, op, value = parse_expr(atom)
            assert op == '='
            part[name] = value
        yield part

def parse_expr(s):
    s = s.replace('=', ' = ')
    s = s.replace('<', ' < ')
    s = s.replace('>', ' > ')
    tokens = s.split()
    return tokens[0], tokens[1], int(tokens[2])

def accepted(workflows, part, name='in'):
    if name == 'R':
        return False
    if name == 'A':
        return True
    for out, expr in workflows[name]:
        if test(expr, part):
            return accepted(workflows, part, out)

def test(expr, part):
    if expr is None:
        return True
    name, op, value = expr
    if op == '<':
        return part[name] < value
    if op == '>' and part[name] > value:
        return part[name] > value

def accepted_super(workflows, superpart, name='in'):
    if name == 'R':
        return []
    if name == 'A':
        return [superpart]
    result = []
    for out, expr in workflows[name]:
        passed, failed = split(expr, superpart)
        if passed is not None:
            result.extend(accepted_super(workflows, passed, out))
        if failed is None:
            return result
        superpart = failed

def split(expr, superpart):
    if expr is None:
        return superpart, None
    name, op, value = expr
    if op == '<' and superpart[name].start < value:
        if superpart[name].stop <= value:
            return superpart, None
        else:
            return set_stop(superpart, name, value), set_start(superpart, name, value)
    if op == '>' and superpart[name].stop >= value:
        if superpart[name].start > value:
            return superpart, None
        else:
            return set_start(superpart, name, value + 1), set_stop(superpart, name, value + 1)
    return None, superpart

def set_stop(superpart, name, stop):
    copy = superpart.copy()
    copy[name] = range(copy[name].start, stop)
    return copy

def set_start(superpart, name, start):
    copy = superpart.copy()
    copy[name] = range(start, copy[name].stop)
    return copy

if __name__ == '__main__':
    aoc.main()
