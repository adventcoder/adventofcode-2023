import aoc
import re

names = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
forward_regex = re.compile('[0-9]|' + '|'.join(re.escape(name) for name in names))
backward_regex = re.compile('[0-9]|' + '|'.join(re.escape(name[::-1]) for name in names))

@aoc.puzzle()
def part1(inp):
    return sum(calibration_value(s) for s in inp.splitlines())

def calibration_value(s):
    first_digit = next(c for c in s if c.isdigit())
    last_digit = next(c for c in reversed(s) if c.isdigit())
    return int(first_digit + last_digit)

@aoc.puzzle()
def part2(inp):
    return sum(real_calibration_value(s) for s in inp.splitlines())

def real_calibration_value(s):
    first_digit = digit(forward_regex.search(s).group())
    last_digit = digit(backward_regex.search(s[::-1]).group()[::-1])
    return int(first_digit + last_digit)

def digit(s):
    return s if s.isdigit() else str(names.index(s))

if __name__ == '__main__':
    aoc.main()
