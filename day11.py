import aoc

@aoc.puzzle()
def part1(inp):
    return solve(inp, 2)

@aoc.puzzle()
def part2(inp):
    return solve(inp, 1000000)

def solve(inp, factor):
    grid = inp.splitlines()
    return total_distance(grid, factor) + total_distance(zip(*grid), factor)

def total_distance(rows, factor):
    N = 0
    S1 = 0
    S2 = 0
    y = 0
    for row in rows:
        n = row.count('#')
        N += n
        S1 += (2*N - n)*n*y
        S2 += n*y
        y += factor**(n==0)
    return S1 - N*S2

if __name__ == '__main__':
    aoc.main()
