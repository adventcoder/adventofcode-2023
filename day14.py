import aoc

#TODO: cleanup

@aoc.puzzle()
def part1(inp):
    grid = inp.splitlines()
    balls = set((x, y) for y, line in enumerate(grid) for x, c in enumerate(line) if c == 'O')
    slide_north(balls, grid)
    return north_load(balls, grid)

@aoc.puzzle()
def part2(inp, target=1000000000):
    grid = inp.splitlines()
    balls = set((x, y) for y, line in enumerate(grid) for x, c in enumerate(line) if c == 'O')
    seen = {}
    cycles = 0
    while cycles < target:
        key = tuple(sorted(balls))
        if key in seen:
            prev_cycles = seen[key]
            target = cycles + (target - prev_cycles) % (cycles - prev_cycles)
            break
        seen[key] = cycles
        slide_north(balls, grid)
        slide_west(balls, grid)
        slide_south(balls, grid)
        slide_east(balls, grid)
        cycles += 1
    while cycles < target:
        slide_north(balls, grid)
        slide_west(balls, grid)
        slide_south(balls, grid)
        slide_east(balls, grid)
        cycles += 1
    return north_load(balls, grid)

def north_load(balls, grid):
    return sum(len(grid) - y for _, y in balls)

def slide_north(balls, grid):
    for x, y in sorted(balls, key=lambda ball: ball[1]):
        balls.remove((x, y))
        while y - 1 >= 0 and grid[y - 1][x] != '#' and (x, y - 1) not in balls:
            y -= 1
        balls.add((x, y))

def slide_south(balls, grid):
    for x, y in sorted(balls, key=lambda ball: ball[1], reverse=True):
        balls.remove((x, y))
        while y + 1 < len(grid) and grid[y + 1][x] != '#' and (x, y + 1) not in balls:
            y += 1
        balls.add((x, y))

def slide_west(balls, grid):
    for x, y in sorted(balls, key=lambda ball: ball[0]):
        balls.remove((x, y))
        while x - 1 >= 0 and grid[y][x - 1] != '#' and (x - 1, y) not in balls:
            x -= 1
        balls.add((x, y))

def slide_east(balls, grid):
    for x, y in sorted(balls, key=lambda ball: ball[0], reverse=True):
        balls.remove((x, y))
        while x + 1 < len(grid[y]) and grid[y][x + 1] != '#' and (x + 1, y) not in balls:
            x += 1
        balls.add((x, y))

if __name__ == '__main__':
    aoc.main()
