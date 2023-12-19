
class Lattice:
    def __init__(self, start=0, step=1):
        self.start = start % step
        self.step = step

    def __repr__(self):
        return f'{type(self).__name__}({self.start}, {self.step})'

    def __contains__(self, n):
        return (n - self.start) % self.step == 0

    def __getitem__(self, i):
        return self.start + i * self.step

    def __and__(self, other):
        d, n1, n2 = bezout(self.step, -other.step)
        if (other.start - self.start) % d != 0:
            raise ValueError(f'{self} & {other}')
        r = (other.start - self.start) // d
        assert self[r*n1] == other[r*n2]
        return Lattice(self[r*n1], self.step*other.step//d)

def bezout(a, b):
    d1, n1, m1 = abs(a), sgn(a), 0
    d2, n2, m2 = abs(b), 0, sgn(b)
    while d2 != 0:
        q = d1 // d2
        d1, d2 = d2, d1 - q*d2
        n1, n2 = n2, n1 - q*n2
        m1, m2 = m2, m1 - q*m2
    return d1, n1, m1

def sgn(x):
    return (x>=0) - (x<=0)
