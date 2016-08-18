from Atom import Atom
from math import sqrt, fabs

class Plane:
    def __init__(self, A, B, C, D):
        self.A = A
        self.B = B
        self.C = C
        self.D = D

    def dist(self,atom):
        if isinstance(atom,Atom):
            d = sqrt( self.A * self.A + self.B * self.B + self.C * self.C)
            s = fabs(self.A * atom.x + self.B * atom.y + self.C * atom.z + self.D)
            return s/d
        else:
            return  0.0

    def contains_atom(self, atom, eps = 0.1):
        return fabs(self.A*atom.x + self.B*atom.y + self.C*atom.z + self.D) < eps

    def __str__(self):
        return 'A={u.A} B={u.B} C={u.C} D={u.D}'.format(u=self)

