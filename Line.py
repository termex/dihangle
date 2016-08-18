from Atom import Atom

class Line:

    def __init__(self, p1, p2):
        if isinstance(p1,Atom) and isinstance(p2,Atom):
            tg = (p2.y-p1.y)/(p2.x-p1.x)
            self.m = tg
            self.c = -tg*p1.x + p1.y

    def f(self,x):
        return self.m * x + self.c

    def under_atoms(self,atoms,toly):

        for a in atoms:
            if self.f(a.x) < a.y-toly:
                return False

        return True