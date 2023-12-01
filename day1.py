import aoc

spellings = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

@aoc.puzzle()
def part1(doc):
    return sum(calibration_value(digits(line)) for line in doc.splitlines())

@aoc.puzzle()
def part2(doc):
    return sum(calibration_value(digits_with_spellings(line)) for line in doc.splitlines())

def calibration_value(digits):
    return digits[0] * 10 + digits[-1]

def digits(line):
    return [int(c) for c in line if c.isdigit()]

def digits_with_spellings(line):
    digits = []
    for i in range(len(line)):
        if line[i].isdigit():
            digits.append(int(line[i]))
        else:
            for digit, spelling in enumerate(spellings):
                if line[i : i + len(spelling)] == spelling:
                    digits.append(digit)
    return digits

if __name__ == '__main__':
    aoc.main()
