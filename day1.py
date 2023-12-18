import aoc

@aoc.puzzle()
def part1(inp):
    return sum(calibration_value(line, None) for line in inp.splitlines())

@aoc.puzzle()
def part2(inp):
    names = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
    return sum(calibration_value(line, names) for line in inp.splitlines())

def calibration_value(s, names):
    return int(find_digit(s, names) + rfind_digit(s, names))

def find_digit(s, names):
    for i, c in enumerate(s):
        if c.isdigit():
            return c
        if names is not None:
            for d, name in enumerate(names):
                if c == name[0] and s[i:i+len(name)] == name:
                    return str(d)

def rfind_digit(s, names):
    for i, c in enumerate(reversed(s)):
        if c.isdigit():
            return c
        if names is not None:
            for d, name in enumerate(names):
                if c == name[-1] and s[len(s)-len(name)-i:len(s)-i] == name:
                    return str(d)

if __name__ == '__main__':
    aoc.main()
