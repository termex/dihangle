from Atom import Atom
from Plane import Plane
from visual import *

class NanoCluster:

    def __init__(self, sirfile):

        infile = open(sirfile,'r')
        self.atoms = []
        self.types = []

        for line in infile:
            if line.lower().find('sphere') != -1:
                str_spl = line.split()
                symbol = str_spl[1]
                x = float(str_spl[2])
                y = float(str_spl[3])
                z = float(str_spl[4])
                col = str_spl[5]
                rad = float(str_spl[6])
                atom = Atom(x,y,z,symbol,rad,col)

                self.atoms.append(atom)

                if symbol not in self.types:
                    self.types.append(symbol)

        infile.close()

        self.numatoms = len(self.atoms)
        self.numtypes = len(self.types)

    def visualize(self):
        for a in self.atoms:
            sphere(pos = (a.x, a.y, a.z), radius = a.radius, color = a.get_rgbcolor())

    def translate(self,vec):
        for a in self.atoms:
            a.translate(vec)

    def rotate(self, fi, along):
        for a in self.atoms:
            a.rotate(fi,along)

    def get_plane_atoms(self, plane, eps = 1.0):
        p_atoms = []

        if isinstance(plane,Plane):
            for a in self.atoms:
                if plane.contains_atom(a,eps) and a.y >= 0.0:
                    p_atoms.append(a)

        return p_atoms

    def visualize_plane_atoms(self,plane,eps = 1.0):
        p_atoms = self.get_plane_atoms(plane, eps)

        for a in p_atoms:
            sphere(pos=(a.x, a.y, a.z), radius = a.radius, color = a.get_rgbcolor())

    def get_maxmin(self):
        xmax = self.atoms[0].x
        ymax = self.atoms[0].y
        zmax = self.atoms[0].z
        xmin = self.atoms[0].x
        ymin = self.atoms[0].y
        zmin = self.atoms[0].z

        for a in self.atoms:
            if xmax < a.x:
                xmax = a.x
            if xmin > a.x:
                xmin = a.x
            if ymax < a.y:
                ymax = a.y
            if ymin > a.y:
                ymin = a.y
            if zmax < a.z:
                zmax = a.z
            if zmin > a.z:
                zmin = a.z

        return (xmax, ymax, zmax), (xmin, ymin, zmin)

    def centrate(self):
        xc = 0.0
        yc = 0.0
        zc = 0.0

        for a in self.atoms:
            xc += a.x
            yc += a.y
            zc += a.z

        N = self.numatoms
        xc /= N
        yc /= N
        zc /= N

        self.translate((-xc,-yc,-zc))




