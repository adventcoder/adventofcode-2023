import aoc
from functools import cache

@aoc.puzzle()
def part1(inp):
    return sum(arrangements(row, runs) for row, runs in map(parse, inp.splitlines()))

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

# 
# Construct an NFA with runs r1,..,rm:
#
# [.?]* [#?]{r1} [.?]+ ... [.?]+ [#?]{rm} [.?]*
#
# For example with runs = (2,1):
#
#    .?                      .?              .?
#   / \                     / \             / \
#   v /                     v /             v /
#   0 ----> 1 ----> 2 ----> 3 ----> 4 ----> 5
#      .?      #?      #?      .?      #?
#
def arrangements_nfa(row, runs):
    blocks = [False]
    for run in runs:
        blocks.extend([True] * run)
        blocks.append(False)
    counts = [0] * (sum(runs) + len(runs) + 1)
    counts[0] = 1
    counts[1] = 1
    active = set([0, 1])
    next_active = set()
    for c in row:
        for i in sorted(active, reverse=True):
            if blocks[i]:
                if c != '.':
                    counts[i + 1] += counts[i]
                    next_active.add(i + 1)
                counts[i] = 0
            else:
                if c == '#':
                    counts[i] = 0
                else:
                    if i + 1 < len(counts):
                        counts[i + 1] += counts[i]
                        next_active.add(i + 1)
                    # counts[i] = counts[i]
                    next_active.add(i)
        active, next_active = next_active, active
        next_active.clear()
    return counts[-1]

def arrangements_nfa2(row, runs):
    dots = [0] * (len(runs) + 1)
    blocks = [[0] * run for run in runs]
    dots[0] = 1
    blocks[0][0] = 1
    for c in row:
        if c == '#':
            fill(dots, 0)
        if c == '.':
            for block in blocks:
                fill(block, 0)
        for i in reversed(range(len(blocks))):
            dots[i+1] += pushpop(blocks[i], dots[i])
    return dots[len(runs)]

def fill(lst, x):
    for i in range(len(lst)):
        lst[i] = x

def pushpop(lst, x):
    lst.insert(0, x)
    return lst.pop()

if __name__ == '__main__':
    aoc.main()

