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

def ways(T, D):
    # t(T-t) > D
    # (T-Δ)/2 < t < (T+Δ)/2, Δ=sqrt(T^2-4D)
    Δ = sqrt(T*T - 4*D)
    tmin = floor((T - Δ)/2) + 1
    tmax = ceil((T + Δ)/2) - 1
    return tmax - tmin + 1

if __name__ == '__main__':
    aoc.main()
