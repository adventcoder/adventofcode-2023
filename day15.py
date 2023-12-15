import aoc

@aoc.puzzle()
def part1(inp):
    return sum(map(hash, steps(inp)))

@aoc.puzzle()
def part2(inp):
    hashmap = Hashmap()
    for step in steps(inp):
        if step[-1] == '-':
            hashmap.clear(step[:-1])
        else:
            label, value = step.split('=')
            hashmap.store(label, int(value))
    return hashmap.power()

def steps(inp):
    return inp.strip().split(',')

def hash(s):
    val = 0
    for c in s:
        val = (val + ord(c)) * 17 % 256
    return val

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

    def power(self):
        total = 0
        for i, box in enumerate(self.boxes):
            _, values = box
            for j, value in enumerate(values):
                total += (i+1)*(j+1)*value
        return total

if __name__ == '__main__':
    aoc.main()
