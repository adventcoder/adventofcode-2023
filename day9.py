import aoc

@aoc.puzzle()
def part1(inp):
    return sum(next(history(line)) for line in inp.splitlines())

@aoc.puzzle()
def part2(inp):
    return sum(next(history(line)[::-1]) for line in inp.splitlines())

def history(line):
    return list(map(int, line.split()))

def next(vals):
    new_val = 0
    while any(val != 0 for val in vals):
        for i in range(len(vals) - 1):
            vals[i] = vals[i + 1] - vals[i]
        new_val += vals.pop()
    return new_val

if __name__ == '__main__':
    aoc.main()
