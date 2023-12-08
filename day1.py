import aoc
import re

digit_names = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

@aoc.puzzle()
def part1(inp):
    return sum(int(find_digit(s) + find_digit(reversed(s))) for s in inp.splitlines())

def find_digit(s):
    return next(filter(str.isdigit, s))

@aoc.puzzle()
def part2(inp):
    lines = inp.splitlines()
    first_digits = map(digit_finder(digit_names), lines)
    last_digits = map(digit_finder([name[::-1] for name in digit_names]), (line[::-1] for line in lines))
    return sum(int(a + b) for a, b in zip(first_digits, last_digits))

def digit_finder(names):
    regex = re.compile('|'.join([r'[0-9]'] + [re.escape(name) for name in names]))
    def find_digit(s):
        group = regex.search(s).group()
        return group if group.isdigit() else str(names.index(group))
    return find_digit

if __name__ == '__main__':
    aoc.main()
