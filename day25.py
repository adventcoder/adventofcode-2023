import aoc
from collections import defaultdict, deque

#TODO: actually solve

@aoc.puzzle()
def part1(inp):
    graph = defaultdict(set)
    for line in inp.splitlines():
        name, connected = line.split(': ')
        for output in connected.split():
            graph[name].add(output)
            graph[output].add(name)

    # dot -Tpng -o day25.png -Kneato day25.dot
    with open('day25.dot', 'w') as file:
        print('graph {', file=file)
        seen = set()
        for name in graph:
            print(f'{name};', file=file)
            for other in graph[name]:
                if other not in seen:
                    print(f'{name} -- {other};', file=file)
            seen.add(name)
        print('}', file=file)

    # By inspection :)
    cut(graph, 'ddl/lcm')
    cut(graph, 'qnd/mbk')
    cut(graph, 'rrl/pcs')

    island1 = flood(graph, 'ddl')
    island2 = flood(graph, 'lcm')
    return len(island1) * len(island2)

def cut(graph, edge):
    a, b = edge.split('/')
    graph[a].remove(b)
    graph[b].remove(a)

def flood(graph, name):
    queue = deque()
    seen = set()
    queue.append(name)
    seen.add(name)
    while queue:
        name = queue.popleft()
        for output in graph[name]:
            if output not in seen:
                queue.append(output)
                seen.add(output)
    return seen

if __name__ == '__main__':
    aoc.main()
