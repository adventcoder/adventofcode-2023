import aoc

dx = [1, 0, -1,  0]
dy = [0, 1,  0, -1]

@aoc.puzzle()
def part1(inp):
    return area(plan(inp))

@aoc.puzzle()
def part2(inp):
    return area((code & 0xF, code >> 4, 0) for _, _, code in plan(inp))

def plan(inp):
    for line in inp.splitlines():
        args = line.split()
        yield 'RDLU'.index(args[0]), int(args[1]), int(args[2][2:-1], 16)

def area(plan):
    edge = 0 # area of exterior
    area = 0 # 2*(area of the interior + area of inner half of the exterior)
    x, y = 0, 0
    for d, n, _ in plan:
        px, x = x, x + n*dx[d]
        py, y = y, y + n*dy[d]
        area += px*y - x*py
        edge += n
    assert (x, y) == (0, 0)
    return (area + edge)//2 + 1

if __name__ == '__main__':
    aoc.main()
