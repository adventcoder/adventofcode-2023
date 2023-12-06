import aoc
from functools import reduce

@aoc.puzzle()
def part1(inp):
    chunks = inp.split('\n\n')
    mappings = list(map(parse_mapping, chunks[1:]))
    seeds = map(int, chunks[0].split()[1:])
    locations = map(lambda seed: reduce(lookup, mappings, seed), seeds)
    return min(locations)

@aoc.puzzle()
def part2(inp):
    chunks = inp.split('\n\n')
    mappings = map(parse_mapping, chunks[1:])
    seeds = list(parse_seed_intervals(chunks[0]))
    locations = reduce(lookup_intervals, mappings, seeds)
    return min(interval.start for interval in locations)

def parse_seeds(line):
    return map(int, line.split()[1:])

def parse_seed_intervals(line):
    values = list(parse_seeds(line))
    for i in range(0, len(values), 2):
        start, size = values[i : i + 2]
        yield range(start, start + size)

def parse_mapping(chunk):
    pairs = []
    for line in chunk.splitlines()[1:]:
        dest_start, source_start, size = map(int, line.split())
        source = range(source_start, source_start + size)
        offset = dest_start - source_start
        pairs.append((source, offset))
    pairs.sort(key=lambda pair: pair[0].start)
    sources, offsets = zip(*pairs)
    for i in range(len(pairs) - 1):
        if sources[i].stop > sources[i + 1].start:
            raise ValueError('overlapping intervals')
    return sources, offsets

def lookup(value, mapping):
    sources, offsets = mapping
    for source, offset in zip(sources, offsets):
        if value in source:
            return value + offset
    return value

def lookup_intervals(values, mapping):
    return [new_value for value in values for new_value in lookup_interval(value, mapping)]

def lookup_interval(value, mapping):
    sources, offsets = mapping
    for source, offset in zip(sources, offsets):
        if overlap := intersect(source, value):
            yield range(overlap.start + offset, overlap.stop + offset)
    if value.start < sources[0].start:
        yield range(value.start, sources[0].start)
    for i in range(len(sources) - 1):
        gap = range(sources[i].stop, sources[i + 1].start)
        if overlap := intersect(gap, value):
            yield overlap
    if value.stop > sources[-1].stop:
        yield range(sources[-1].stop, value.stop)

def intersect(a, b):
    return range(max(a.start, b.start), min(a.stop, b.stop))

if __name__ == '__main__':
    aoc.main()
