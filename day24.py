import aoc

@aoc.puzzle()
def part1(inp, min=200000000000000, max=400000000000000):
    rays = parse_rays(inp)
    count = 0
    for i in range(len(rays)):
        for j in range(i+1, len(rays)):
            (px1, py1, _), (vx1, vy1, _) = rays[i]
            (px2, py2, _), (vx2, vy2, _) = rays[j]
            #
            # P1 + t1 V1 = P2 + t2 V2
            #
            #          t1 V1 = t2 V2 + P2-P1
            # t1 V1.perp(V2) = (P2-P1).perp(V2)
            #             t1 = (P2-P1).perp(V2)/V1.perp(V2)
            #
            #          t2 V2 = t1 V1 + P1-P2
            # t2 V2.perp(V1) = (P1-P2).perp(V1)
            #             t2 = (P1-P2).perp(V1)/V2.perp(V1)
            #
            d = vx2*vy1 - vy2*vx1
            if d == 0:
                continue
            t1 = (vx2*(py2-py1) - vy2*(px2-px1)) / d
            t2 = (vx1*(py2-py1) - vy1*(px2-px1)) / d
            if t1 > 0 and t2 > 0:
                px = px1 + t1*vx1
                py = py1 + t1*vy1
                if min <= px <= max and min <= py <= max:
                    count += 1
    return count

@aoc.puzzle()
def part2(inp):
    rays = parse_rays(inp)
    #
    # Pi + ti Vi = P + t V
    # (Pi-P) + ti (Vi-V) = 0
    # (Pi-P)x(Vi-V) = 0
    #
    # ((Pi-P)x(Pj-P)).(Vi-Vj) = 0
    #
    # ((Pi-Pj)x(Vi-Vj)).P + (PixPj).(Vi-Vj) = 0
    #
    # [(P1-P2)x(V1-V2)]     [(P1xP2).(V1-V2)]
    # [(P1-P3)x(V1-V3)] P + [(P1xP3).(V1-V3)] = 0
    # [(P2-P3)x(V2-V3)]     [(P2xP3).(V2-V3)]
    #
    A = []
    b = []
    for i in range(3):
        for j in range(i + 1, 3):
            Pi, Vi = rays[i]
            Pj, Vj = rays[j]
            A.append(cross(sub(Pi, Pj), sub(Vi, Vj)))
            b.append(-dot(cross(Pi, Pj), sub(Vi, Vj)))
    return sum(solve(A, b))

def sub(v1, v2):
    (x1, y1, z1) = v1
    (x2, y2, z2) = v2
    return x1 - x2, y1 - y2, z1 - z2

def cross(v1, v2):
    (x1, y1, z1) = v1
    (x2, y2, z2) = v2
    return y1*z2 - z1*y2, z1*x2 - x1*z2, x1*y2 - y1*x2

def dot(v1, v2):
    (x1, y1, z1) = v1
    (x2, y2, z2) = v2
    return x1*x2 + y1*y2 + z1*z2

def solve(A, b):
    r1, r2, r3 = A
    c1 = cross(r2, r3)
    c2 = cross(r3, r1)
    c3 = cross(r1, r2)
    det = dot(r1, c1) # = -dot(r2, c2) = dot(r3, c3)
    return [dot(r, b) // det for r in zip(c1, c2, c3)]

def parse_rays(inp):
    rays = []
    for line in inp.splitlines():
        s1, s2 = line.split('@')
        pos = tuple(map(int, s1.split(',')))
        vel = tuple(map(int, s2.split(',')))
        rays.append((pos, vel))
    return rays

if __name__ == '__main__':
    aoc.main()
