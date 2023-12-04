import aoc

words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

@aoc.puzzle()
def part1(inp):
    return sum(calibration_value(s) for s in inp.splitlines())

@aoc.puzzle()
def part2(inp):
    return sum(real_calibration_value(s) for s in inp.splitlines())

def calibration_value(s):
    ds = [c for c in s if c.isdigit()]
    return int(ds[0] + ds[-1])

def real_calibration_value(s):
    for d1, word1 in enumerate(words):
        for d2, word2 in enumerate(words):
            if word1[-1] == word2[0]:
                s = s.replace(word1 + word2[1:], str(d1) + str(d2))
    for d, word in enumerate(words):
        s = s.replace(word, str(d))
    return calibration_value(s)

if __name__ == '__main__':
    aoc.main()
