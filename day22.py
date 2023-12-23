import aoc
from collections import deque, namedtuple

Brick = namedtuple('Brick', ('xs', 'ys', 'zs'))

@aoc.puzzle()
def part1(inp):
    bricks = parse_bricks(inp)
    graph = build_graph(bricks)
    return sum(graph.safe(i) for i in range(len(bricks)))

@aoc.puzzle()
def part2(inp):
    bricks = parse_bricks(inp)
    graph = build_graph(bricks)
    return sum(graph.chain_size(i) for i in range(len(bricks)))

def parse_bricks(inp):
    bricks = []
    for line in inp.splitlines():
        s1, s2 = line.split('~')
        x1, y1, z1 = map(int, s1.split(','))
        x2, y2, z2 = map(int, s2.split(','))
        xs = range(min(x1, x2), max(x1, x2) + 1)
        ys = range(min(y1, y2), max(y1, y2) + 1)
        zs = range(min(z1, z2), max(z1, z2) + 1)
        bricks.append(Brick(xs, ys, zs))
    bricks.sort(key=lambda brick: brick.zs.start)
    return bricks

def build_graph(bricks):
    tower = [{}] # floor
    above = []
    below = []
    for i, brick in enumerate(bricks):
        # Find how far the brick drops
        start_z = len(tower)
        while start_z > 1 and all((x, y) not in tower[start_z - 1] for x in brick.xs for y in brick.ys):
            start_z -= 1
        stop_z = start_z + len(brick.zs)

        # Add the brick to the tower
        while len(tower) < stop_z:
            tower.append({})
        for z in range(start_z, stop_z):
            for x in brick.xs:
                for y in brick.ys:
                    tower[z][(x, y)] = i

        # Add the brick to the graph
        above.append(set())
        below.append(set())
        for x in brick.xs:
            for y in brick.ys:
                if (x, y) in tower[start_z - 1]:
                    j = tower[start_z - 1][(x, y)]
                    below[i].add(j)
                    above[j].add(i)

    return Graph(above, below)

class Graph:
    def __init__(self, above, below):
        self.above = above
        self.below = below

    def settled(self, i, destroyed):
        return len(self.below[i] - destroyed) > 0

    def safe(self, i):
        return all(self.settled(j, { i }) for j in self.above[i])

    def chain_size(self, i):
        destroyed = { i }
        queue = deque(self.above[i])
        while queue:
            i = queue.popleft()
            if i not in destroyed and not self.settled(i, destroyed):
                destroyed.add(i)
                queue.extend(self.above[i])
        return len(destroyed) - 1

if __name__ == '__main__':
    aoc.main()
