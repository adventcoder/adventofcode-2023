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
    first_digit = digit_finder(digit_names)
    last_digit = digit_finder(name[::-1] for name in digit_names)
    return sum(int(first_digit(s) + last_digit(s[::-1])) for s in inp.splitlines())

def digit_finder(names):
    digits = {}
    for d, name in enumerate(names):
        digits[name] = str(d)
    regex = re.compile('|'.join([r'[0-9]', *map(re.escape, digits.keys())]))
    def find_digit(s):
        group = regex.search(s).group()
        return group if group.isdigit() else digits[group]
    return find_digit

if __name__ == '__main__':
    aoc.main()
