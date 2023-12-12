import aoc
from functools import cache

@aoc.puzzle()
def part1(inp):
    return sum(arrangements(*parse(line)) for line in inp.splitlines())

@aoc.puzzle()
def part2(inp):
    return sum(arrangements(*unfold(*parse(line))) for line in inp.splitlines())

def parse(line):
    row, runs = line.split()
    return row, tuple(map(int, runs.split(',')))

def unfold(row, runs):
    return '?'.join([row]*5), runs*5

def arrangements(row, runs):
    ri = row.rfind('#')
    max_run = [0] * len(row)
    for i in reversed(range(len(row))):
        if row[i] in '#?':
            max_run[i] = (max_run[i + 1] if i + 1 < len(row) else 0) + 1
    @cache
    def recur(i, j):
        if j == len(runs):
            if i > ri:
                return 1
            return 0
        elif i == len(row):
            return 0
        else:
            count = 0
            if row[i] in '.?':
                count += recur(i + 1, j)
            if row[i] in '#?' and runs[j] <= max_run[i]:
                if i + runs[j] == len(row):
                    count += recur(i + runs[j], j + 1)
                elif row[i + runs[j]] in '.?':
                    count += recur(i + runs[j] + 1, j + 1)
            return count
    return recur(0, 0)

if __name__ == '__main__':
    aoc.main()

