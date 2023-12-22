import aoc
from dataclasses import dataclass
from collections import defaultdict, deque

@aoc.puzzle()
def part1(inp):
    tower = Tower(inp)
    return sum(tower.safe(brick) for brick in tower.bricks)

@aoc.puzzle()
def part2(inp):
    tower = Tower(inp)
    return sum(tower.destroy(brick) for brick in tower.bricks)

@dataclass(frozen=True)
class Brick:
    xs: range
    ys: range
    zs: range

def parse_brick(line):
    s1, s2 = line.split('~')
    x1, y1, z1 = map(int, s1.split(','))
    x2, y2, z2 = map(int, s2.split(','))
    xs = range(min(x1, x2), max(x1, x2) + 1)
    ys = range(min(y1, y2), max(y1, y2) + 1)
    zs = range(min(z1, z2), max(z1, z2) + 1)
    return Brick(xs, ys, zs)

class Tower:
    def __init__(self, inp):
        self.bricks = []
        self.layers = defaultdict(dict)
        for brick in sorted(map(parse_brick, inp.splitlines()), key=lambda brick: brick.zs.start):
            self.drop(brick)

    def drop(self, brick):
        start_z = brick.zs.start
        while start_z > 1 and not self.intersect(brick.xs, brick.ys, start_z - 1):
            start_z -= 1
        zs = range(start_z, start_z + len(brick.zs))
        for z in zs:
            for x in brick.xs:
                for y in brick.ys:
                    self.layers[z][(x, y)] = len(self.bricks)
        self.bricks.append(Brick(brick.xs, brick.ys, zs))

    def intersect(self, xs, ys, z):
        bricks = set()
        for x in xs:
            for y in ys:
                if (x, y) in self.layers[z]:
                    i = self.layers[z][(x, y)]
                    bricks.add(self.bricks[i])
        return bricks

    def below(self, brick):
        return self.intersect(brick.xs, brick.ys, brick.zs.start - 1)

    def above(self, brick):
        return self.intersect(brick.xs, brick.ys, brick.zs.stop)

    def settled(self, brick, destroyed):
        return len(self.below(brick) - destroyed) > 0

    def safe(self, brick):
        return all(self.settled(b, { brick }) for b in self.above(brick))

    def destroy(self, brick):
        destroyed = { brick }
        queue = deque(self.above(brick))
        while queue:
            brick = queue.popleft()
            if brick not in destroyed and not self.settled(brick, destroyed):
                destroyed.add(brick)
                queue.extend(self.above(brick))
        return len(destroyed) - 1

if __name__ == '__main__':
    aoc.main()
