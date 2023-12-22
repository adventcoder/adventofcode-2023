import aoc
from dataclasses import dataclass
from collections import deque

#TODO: overengineered, could be simplified?

@aoc.puzzle()
def part1(inp):
    stack = settle(inp)
    return sum(stack.safe(i) for i in stack.lines())

@aoc.puzzle()
def part2(inp):
    stack = settle(inp)
    return sum(stack.pull(i) for i in stack.lines())

@dataclass
class Brick:
    xs: range
    ys: range
    zs: range

    def move(self, z):
        return Brick(self.xs, self.ys, range(z, z + len(self.zs)))

def settle(inp):
    stack = Stack()
    bricks = []
    for line in inp.splitlines():
        bricks.append(parse_brick(line))
    bricks.sort(key=lambda b: b.zs.start)
    for brick in bricks:
        stack.drop(brick)
    return stack

def parse_brick(line):
    s1, s2 = line.split('~')
    x1, y1, z1 = map(int, s1.split(','))
    x2, y2, z2 = map(int, s2.split(','))
    xs = range(min(x1, x2), max(x1, x2) + 1)
    ys = range(min(y1, y2), max(y1, y2) + 1)
    zs = range(min(z1, z2), max(z1, z2) + 1)
    return Brick(xs, ys, zs)

class Stack:
    def __init__(self):
        self.settled = []
        self.above = []
        self.below = []

    def drop(self, brick):
        stop_z = 1
        supports = []
        for i, support in enumerate(self.settled):
            if overlaps(brick.xs, support.xs) and overlaps(brick.ys, support.ys):
                assert brick.zs.start >= support.zs.stop
                if support.zs.stop > stop_z:
                    supports = [i]
                    stop_z = support.zs.stop
                elif support.zs.stop == stop_z:
                    supports.append(i)
        j = len(self.settled)
        self.settled.append(brick.move(stop_z))
        self.below.append(supports)
        self.above.append([])
        for i in supports:
            self.above[i].append(j)

    def lines(self):
        return range(len(self.settled))

    def safe(self, i):
        return all(self.supported(j, {i}) for j in self.above[i])

    def pull(self, i):
        removed = set()
        queue = deque()
        removed.add(i)
        queue.extend(self.above[i])
        while queue:
            i = queue.popleft()
            if i not in removed and not self.supported(i, removed):
                removed.add(i)
                queue.extend(self.above[i])
        return len(removed) - 1

    def supported(self, i, removed):
        return any(j not in removed for j in self.below[i])

def overlaps(r1, r2):
    return r1.start < r2.stop and r2.start < r1.stop

def print_sideviews(bricks):
    x_stop = max(b.xs.stop for b in bricks)
    y_stop = max(b.ys.stop for b in bricks)
    z_stop = max(b.zs.stop for b in bricks)
    x_grid = [['.'] * x_stop for _ in range(z_stop)]
    y_grid = [['.'] * x_stop for _ in range(z_stop)]
    for i, b in enumerate(bricks):
        c = chr(ord('A') + i)
        for z in b.zs:
            for x in b.xs:
                x_grid[z][x] = c if x_grid[z][x] == '.' else '?'
            for y in b.ys:
                y_grid[z][y] = c if y_grid[z][y] == '.' else '?'
    for x in range(x_stop):
        x_grid[0][x] = '-'
    for y in range(y_stop):
        y_grid[0][y] = '-'
    print('x'.center(x_stop), ' ', 'y'.center(y_stop))
    for z in reversed(range(z_stop)):
        print(''.join(x_grid[z]), ' ', ''.join(y_grid[z]), z)

if __name__ == '__main__':
    aoc.main()
