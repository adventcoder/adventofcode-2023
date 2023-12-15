import aoc

@aoc.puzzle()
def part1(inp):
    return sum(hash(step) for step in inp.strip().split(','))

@aoc.puzzle()
def part2(inp):
    hashmap = Hashmap()
    for step in inp.strip().split(','):
        if step[-1] == '-':
            hashmap.clear(step[:-1])
        else:
            label, value = step.split('=')
            hashmap.store(label, int(value))
    return sum((i+1)*(j+1)*value for i, (_, values) in enumerate(hashmap.boxes) for j, value in enumerate(values))

def hash(s):
    value = 0
    for c in s:
        value = (value + ord(c)) * 17 % 256
    return value

class Hashmap:
    def __init__(self):
        self.boxes = [([], []) for _ in range(256)]

    def store(self, label, value):
        labels, values = self.boxes[hash(label)]
        if label in labels:
            values[labels.index(label)] = value
        else:
            labels.append(label)
            values.append(value)

    def clear(self, label):
        labels, values = self.boxes[hash(label)]
        if label in labels:
            i = labels.index(label)
            labels.pop(i)
            values.pop(i)

if __name__ == '__main__':
    aoc.main()
