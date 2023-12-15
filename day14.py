import aoc
import click

@aoc.puzzle()
def part1(inp):
    grid = parse_grid(inp)
    rotate_clockwise(grid)
    tilt_east(grid)
    return load_east(grid)

@aoc.puzzle()
@click.option('--verbose', is_flag=True)
def part2(inp, verbose):
    grid = parse_grid(inp)
    seen = {}
    cycles = 0
    target = 1000000000
    while cycles < target:
        key = make_key(grid)
        if prev_cycles := seen.get(key):
            if verbose:
                print('Cycle start:', prev_cycles)
                print('Cycle length:', cycles - prev_cycles)
            target = cycles + (target - prev_cycles) % (cycles - prev_cycles)
            break
        seen[key] = cycles
        cycle(grid)
        cycles += 1
    while cycles < target:
        cycle(grid)
        cycles += 1
    rotate_clockwise(grid)
    return load_east(grid)

def parse_grid(inp):
    return [list(line) for line in inp.splitlines()]

def make_key(grid):
    return bytes(c == 'O' for row in grid for c in row if c != '#')

def cycle(grid):
    for _ in range(4):
        rotate_clockwise(grid)
        tilt_east(grid)

def rotate_clockwise(grid):
    transpose(grid)
    flip(grid)

def rotate_anticlockwise(grid):
    flip(grid)
    transpose(grid)

def transpose(grid):
    grid[:] = map(list, zip(*grid))

def flip(grid):
    for row in grid:
        row.reverse()

def load_east(grid):
    return sum(x+1 for row in grid for x, c in enumerate(row) if c == 'O')

def tilt_east(grid):
    for row in grid:
        n = 0
        for x in range(len(row)):
            if row[x] == 'O':
                n += 1
            elif row[x] == '#':
                n = 0
            else:
                if n > 0:
                    row[x] = 'O'
                    row[x-n] = '.'
        
if __name__ == '__main__':
    aoc.main()
