import aoc

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
    for d1, word1 in enumerate(digits_as_words):
        for d2, word2 in enumerate(digits_as_words):
            if word1[-1] == word2[0]:
                s = s.replace(word1 + word2[1:], str(d1) + str(d2))
    for d, word in enumerate(digits_as_words):
        s = s.replace(word, str(d))
    return calibration_value(s)

if __name__ == '__main__':
    aoc.main()
