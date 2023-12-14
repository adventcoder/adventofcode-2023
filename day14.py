import aoc

@aoc.puzzle()
def part1(inp):
    grid = [list(line) for line in inp.splitlines()]
    slide_north(grid)
    return north_load(grid)

@aoc.puzzle()
def part2(inp, target=1000000000):
    grid = [list(line) for line in inp.splitlines()]
    seen = {}
    cycles = 0
    while cycles < target:
        key = make_key(grid)
        if prev_cycles := seen.get(key):
            target = cycles + (target - prev_cycles) % (cycles - prev_cycles)
            break
        seen[key] = cycles
        cycle(grid)
        cycles += 1
    while cycles < target:
        cycle(grid)
        cycles += 1
    return north_load(grid)

def make_key(grid):
    return bytes(c == 'O' for row in grid for c in row if c != '#')

def north_load(grid):
    return sum((len(grid) - y)*row.count('O') for y, row in enumerate(grid))

def cycle(grid):
    slide_north(grid)
    slide_west(grid)
    slide_south(grid)
    slide_east(grid)

def slide_north(grid):
    for x in range(len(grid[0])):
        n = 0
        for y in reversed(range(len(grid))):
            if grid[y][x] == 'O':
                n += 1
            elif grid[y][x] == '#':
                n = 0
            else:
                if n > 0:
                    grid[y][x] = 'O'
                    grid[y+n][x] = '.'

def slide_west(grid):
    for row in grid:
        n = 0
        for x in reversed(range(len(row))):
            if row[x] == 'O':
                n += 1
            elif row[x] == '#':
                n = 0
            else:
                if n > 0:
                    row[x] = 'O'
                    row[x+n] = '.'

def slide_south(grid):
    for x in range(len(grid[0])):
        n = 0
        for y in range(len(grid)):
            if grid[y][x] == 'O':
                n += 1
            elif grid[y][x] == '#':
                n = 0
            else:
                if n > 0:
                    grid[y][x] = 'O'
                    grid[y-n][x] = '.'

def slide_east(grid):
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
