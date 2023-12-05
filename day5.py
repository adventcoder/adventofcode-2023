import aoc
from functools import reduce
from math import inf

@aoc.puzzle()
def part1(inp):
    chunks = inp.split('\n\n')
    mappings = [parse_mapping(chunk) for chunk in chunks[1:]]
    min_location = inf
    for seed in parse_ints(chunks[0]):
        location = reduce(lookup, mappings, seed)
        if location < min_location:
            min_location = location
    return min_location

@aoc.puzzle()
def part2(inp):
    chunks = inp.split('\n\n')
    seeds = parse_ints(chunks[0])
    values = []
    for i in range(0, len(seeds), 2):
        start, size = seeds[i : i + 2]
        values.append(Interval(start, start + size - 1))
    for mapping in map(parse_mapping, chunks[1:]):
        values = [new_value for value in values for new_value in lookup_interval(value, mapping)]
    return min(value.start for value in values)

def parse_mapping(chunk):
    mapping = []
    for line in chunk.splitlines()[1:]:
        dest_start, source_start, size = parse_ints(line)
        mapping.append((Interval(source_start, source_start + size - 1), dest_start - source_start))
    mapping.sort(key=lambda pair: pair[0].start)
    return mapping

def parse_ints(s):
    return tuple(int(token) for token in s.split() if token.isdigit())

def lookup(value, mapping):
    for interval, offset in mapping:
        if value in interval:
            return value + offset
    return value

def lookup_interval(value, mapping):
    for interval, offset in mapping:
        if overlap := value & interval:
            yield overlap + offset
    for gap in gaps(mapping):
        if overlap := value & gap:
            yield overlap

def gaps(mapping):
    yield Interval(-inf, mapping[0][0].start - 1)
    for i in range(len(mapping) - 1):
        yield Interval(mapping[i][0].end + 1, mapping[i+1][0].start - 1)
    yield Interval(mapping[-1][0].end + 1, inf)

class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __bool__(self):
        return self.start <= self.end

    def __contains__(self, x):
        return self.start <= x <= self.end

    def __add__(self, offset):
        return Interval(self.start + offset, self.end + offset)

    def __and__(self, other):
        return Interval(max(self.start, other.start), min(self.end, other.end))

if __name__ == '__main__':
    aoc.main()
