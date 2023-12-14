import aoc

@aoc.puzzle()
def part1(inp):
    ans = 0
    for chunk in inp.split('\n\n'):
        grid = chunk.splitlines()
        ans += find_vert_reflection(grid) + 100*find_horz_reflection(grid)
    return ans

@aoc.puzzle()
def part2(inp):
    # TODO: better than bruteforce
    ans = 0
    for chunk in inp.split('\n\n'):
        grid = chunk.splitlines()
        v = find_vert_reflection(grid)
        h = find_horz_reflection(grid)
        for smudge in smudges(grid):
            new_v = find_vert_reflection(smudge, v)
            if new_v != 0:
                ans += new_v
                break
            new_h = find_horz_reflection(smudge, h)
            if new_h != 0:
                ans += new_h * 100
                break
    return ans

def find_horz_reflection(grid, skip=None):
    return find_vert_reflection(list(zip(*grid)), skip)

def find_vert_reflection(grid, skip=None):
    for i in range(1, len(grid[0])):
        if i != skip and all(is_reflection(row, i) for row in grid):
            return i
    return 0

def is_reflection(row, i):
    n = min(i, len(row) - i)
    return all(row[i - 1 - r] == row[i + r] for r in range(n))

def smudges(grid):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == '#':
                yield grid[:y] + [row[:x] + '.' + row[x+1:]] + grid[y+1:]
            elif c == '.':
                yield grid[:y] + [row[:x] + '#' + row[x+1:]] + grid[y+1:]

if __name__ == '__main__':
    aoc.main()
