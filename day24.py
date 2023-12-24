import aoc
from fractions import Fraction

#TODO: cleanup

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
    # P1 + t1 V1 = Ps + t1 Vs
    # P2 + t2 V2 = Ps + t2 Vs
    # P3 + t3 V3 = Ps + t3 Vs
    #
    # Vs = (P1-Ps)/t1 + V1
    #
    # Ps = (t1 P2 - t2 P1 + t1 t2 (V2-V1))/(t1-t2)
    # Ps = (t1 P3 - t3 P1 + t1 t3 (V3-V1))/(t1-t3)
    #
    # t1 (P2-P3) + t2 (P3-P1) + t3 (P1-P2) + t1 t2 (V2-V1) + t1 t3 (V1-V3) + t2 t3 (V3-V2) = 0
    #
    # That's as far as I got. Solved with Mathematica originally.
    #
    #---
    #
    # The idea for using cross product taken from elsewhere.
    #
    # Pi + ti Vi = P + ti V
    # (P-Pi) + ti (V-Vi) = 0
    # (P-Pi)x(V-Vi) + ti (V-Vi)x(V-Vi) = 0
    # PxVi + PixV = PixVi - PxV
    #
    # We can subtract any two pairs of these to get rid of the PxV term and get a system of 6 equations/6 unknowns.
    #
    # Px(Vi-Vj) + (Pi-Pj)xV = PixVi - PjxVj
    #
    # Where [v]x is the cross product matrix:
    #
    # [   :           :  ] [:]   [     :     ]
    # [[Vj-Vi]x  [Pi-Pj]x] [P] = [PixVi-PjxVj]
    # [   :           :  ] [:]   [     :     ]
    #                      [:]
    #                      [V]
    #                      [:]
    #
    # ---
    #
    # Pi + ti Vi = P + ti V
    #  ti (Vi-V) = (P-Pi)
    #         ti = (P-Pi).(Vi-V)/(Vi-V).(Vi-V)
    #
    M = []
    for i in range(2):
        (P1, V1), (P2, V2) = rays[i:i+2]
        for a, b, c in zip(cross_matrix(sub(V2, V1)), cross_matrix(sub(P1, P2)), sub(cross(P1, V1), cross(P2, V2))):
            M.append(a + b + [c])
    row_reduce(M)
    Px, Py, Pz, _, _, _ = list(zip(*M))[-1]
    return Px + Py + Pz

def sub(v1, v2):
    (x1, y1, z1) = v1
    (x2, y2, z2) = v2
    return x1 - x2, y1 - y2, z1 - z2

def cross(v1, v2):
    (x1, y1, z1) = v1
    (x2, y2, z2) = v2
    return y1*z2 - z1*y2, z1*x2 - x1*z2, x1*y2 - y1*x2

def cross_matrix(v):
    x, y, z = v
    return [[0, -z, y], [z, 0, -x], [-y, x, 0]]

def row_reduce(M):
    for i in range(len(M)):
        pivot_row = max(range(i, len(M)), key=lambda x: abs(M[x][i]))
        if M[pivot_row][i] == 0:
            break
        M[i], M[pivot_row] = M[pivot_row], M[i]
        pivot = M[i][i]
        M[i] = [Fraction(x, pivot) for x in M[i]]
        for j in range(len(M)):
            if j != i:
                factor = M[j][i]
                M[j] = [x - factor * y for x, y in zip(M[j], M[i])]
    return M

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
