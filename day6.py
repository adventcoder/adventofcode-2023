import aoc
from math import *

test_input = '''
Time:      7  15   30
Distance:  9  40  200
'''

@aoc.puzzle()
def part1(inp):
    Ts, Ds = [map(int, line.split()[1:]) for line in inp.splitlines()]
    return prod(ways(T, D) for T, D in zip(Ts, Ds))

@aoc.puzzle()
def part2(inp):
    T, D = [int(''.join(line.split()[1:])) for line in inp.splitlines()]
    return ways(T, D)

# t(T-t) > D
# (T/2) - sqrt((T/2)^2-D) < t < (T/2) + sqrt((T/2)^2-D)
def ways(T, D):
    h = T/2
    t_min = floor(h - sqrt(h*h-D)) + 1
    t_max = ceil(h + sqrt(h*h-D)) - 1
    return t_max - t_min + 1

if __name__ == '__main__':
    aoc.main()
