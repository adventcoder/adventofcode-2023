import aoc
from collections import defaultdict, Counter
from math import inf

#TODO: this could be optimised...

@aoc.puzzle()
def part1(inp):
    edges = defaultdict(Counter)
    for line in inp.splitlines():
        a, bs = line.split(':')
        for b in bs.split():
            edges[a][b] = 1
            edges[b][a] = 1
    total = len(edges)
    cut, partition = find_minimum_cut(edges)
    assert cut == 3
    return len(partition) * (total - len(partition))

def find_minimum_cut(edges):
    min_cut = inf
    min_t = None
    while len(edges) > 1:
        s, t, cut = find_minimum_st_cut(edges)
        if cut < min_cut:
            min_cut = cut
            min_t = t
        contract(edges, s, t)
    return min_cut, min_t.split(',')

# Find any minimum s-t cut in the graph (using maximum adjacency search)
# t is a single super vertex representing the sink partition
# s is an arbitrary vertex from the source partition which makes up the rest of the graph
def find_minimum_st_cut(edges):
    # queue ordered by combined weight of edges to the visited set
    queue = { v: 0 for v in edges.keys() }
    t = None
    while queue:
        # Pop the vertex with the most combined edge weight
        s = t
        t = max(queue, key=queue.get)
        cut = queue.pop(t)
        # Add it to the visited set
        for n, w in edges[t].items():
            if n in queue:
                queue[n] += w
    return s, t, cut

def contract(edges, a, b):
    c = ','.join([a, b])
    for n in edges[a]:
        if n != b:
            edges[c][n] += edges[n].pop(a)
    for n in edges[b]:
        if n != a:
            edges[c][n] += edges[n].pop(b)
    for n in edges[c]:
        edges[n][c] = edges[c][n]
    edges.pop(a)
    edges.pop(b)

if __name__ == '__main__':
    aoc.main()
