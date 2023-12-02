import aoc
from collections import defaultdict

digits_as_words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

@aoc.puzzle()
def part1(doc):
    return sum(calibration_value(s) for s in doc.splitlines())

@aoc.puzzle()
def part2(doc):
    return sum(real_calibration_value(s) for s in doc.splitlines())

def calibration_value(s):
    digits = [c for c in s if c.isdigit()]
    return int(digits[0] + digits[-1])

def real_calibration_value(s):
    return int(find_first_digit(s) + find_last_digit(s))

def find_first_digit(s):
    for i in range(len(s)):
        if s[i].isdigit():
            return s[i]
        for d, word in enumerate(digits_as_words):
            if s[i : i + len(word)] == word:
                return str(d)

def find_last_digit(s):
    for i in reversed(range(len(s))):
        if s[i].isdigit():
            return s[i]
        for d, word in enumerate(digits_as_words):
            if s[i + 1 - len(word) : i + 1] == word:
                return str(d)

if __name__ == '__main__':
    aoc.main()
