import aoc

@aoc.puzzle()
def part1(inp):
    return distance_sum(inp.splitlines(), 2)

@aoc.puzzle()
def part2(inp):
    return distance_sum(inp.splitlines(), 1000000)

def distance_sum(grid, factor):
    return distance_sum_major(grid, factor) + distance_sum_major(zip(*grid), factor)

#TODO: can this be cleaner?
def distance_sum_major(grid, factor):
    N = 0
    S1 = 0
    S2 = 0
    y = 0
    for row in grid:
        n = row.count('#')
        N += n
        S1 += (2*N - n)*n*y
        S2 += n*y
        y += factor if n == 0 else 1
    return S1 - N*S2

def distance_sum_major_old(rows, factor):
    ys = []
    y = 0
    for row in rows:
        n = row.count('#')
        ys.append((y, n))
        y += factor if n == 0 else 1
    distance = 0
    for i, (y1, n1) in enumerate(ys):
        for (y2, n2) in ys[i+1:]:
            distance += n1*n2*(y2 - y1)
    return distance

if __name__ == '__main__':
    aoc.main()
