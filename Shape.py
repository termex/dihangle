from Atom import Atom
from math import fabs, atan, pi
from visual import *
import matplotlib.pyplot as plt
import numpy as np
from Line import Line

class Shape:

    def __init__(self, atoms):
        self.shape_atoms = []
        self.xmax = 0.0
        self.ymax = 0.0
        self.max = 0.0

        for a in atoms:
            a.z = 0.0
            self.shape_atoms.append(a)
            abs_x = fabs(a.x)
            abs_y = fabs(a.y)
            if abs_x > self.xmax:
                self.xmax = abs_x
            if abs_y > self.ymax:
                self.ymax = abs_y

        if self.xmax > self.ymax:
            self.max = self.xmax
        else:
            self.max = self.ymax


    def visualize(self):
        for a in self.shape_atoms:
            sphere(pos=(a.x, a.y, a.z), radius=a.radius, color=a.get_rgbcolor())

    def get_xy(self,atoms):
        x = []
        y = []
        for a in atoms:
            x.append(a.x)
            y.append(a.y)
        return x, y

    def visualize2D(self,show_max = False):
        x, y = self.get_xy(self.shape_atoms)
        plt.axis([-self.max-5.0, self.max+5.0,-0.05,self.max+5.0])
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.plot(x,y,'yo')

        if show_max:
            mx = self.get_max_atoms()
            xc = [mx[0].x, mx[1].x]
            yc = [mx[0].y, mx[1].y]
            plt.plot(xc,yc,'go')

        plt.show()

    def visualize_with_selections2D(self, selections, showfit = False):
        x, y = self.get_xy(self.shape_atoms)
        plt.axis([-self.max - 5.0, self.max + 5.0, -0.05, self.max + 5.0])
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.plot(x, y, 'yo')

        for s in selections:
            atoms, style = s
            x, y = self.get_xy(atoms)
            plt.plot(x, y, style)

        if showfit:
            for s in selections:
                atoms, style = s
                x, y = self.get_xy(atoms)
                xnp = np.array(x)
                ynp = np.array(y)
                A = np.vstack([xnp, np.ones(len(xnp))]).T
                m, c = np.linalg.lstsq(A, ynp)[0]
                plt.plot(xnp, m * xnp + c)

        plt.show()

    def find_right_lines(self, tolx = 0.5, toly =0.5, tolm = 0.01):
        al, ar = self.get_max_atoms()
        atoms = self.get_atoms_in_region((0, ar.x + 2.0*tolx))

        lines = []

        for i in xrange(0,len(atoms)):
            for j in xrange(i+1,len(atoms)):
                if fabs(atoms[i].x - atoms[j].x)>tolx:
                    line = Line(atoms[i],atoms[j])
                    if line.under_atoms(atoms,toly) and line.m > 0 and fabs(line.m)>tolm:
                        lines.append(line)

        return lines

    def find_left_lines(self, tolx = 0.5, toly=0.5, tolm = 0.01):
        al, ar = self.get_max_atoms()
        atoms = self.get_atoms_in_region((0,al.x - 2.0*tolx))

        lines = []

        for i in xrange(0,len(atoms)):
            for j in xrange(i+1,len(atoms)):
                if fabs(atoms[i].x - atoms[j].x)>tolx:
                    line = Line(atoms[i],atoms[j])
                    if line.under_atoms(atoms,toly) and line.m < 0 and fabs(line.m)>tolm:
                        lines.append(line)

        return lines


    def fit_line(self, atoms):
        xa, ya = self.get_xy(atoms)
        x = np.array(xa)
        y = np.array(ya)
        A = np.vstack([x, np.ones(len(x))]).T
        return np.linalg.lstsq(A, y)[0]

    def get_correct_angle_atoms(self, atoms):
        n_atoms = []
        m, c = self.fit_line(atoms)
        f = lambda x: m * x + c

        for a in atoms:
            if a.y - f(a.x) >= 0.0:
                n_atoms.append(a)

        return n_atoms

    def average_mc(self, atoms):
        m1,c1 = self.fit_line(atoms)
        cor_atoms = self.get_correct_angle_atoms(atoms)

        if len(cor_atoms) >= 2:
            m2, c2 = self.fit_line(atoms)
            return 0.5 * (m1+m2), 0.5 * (c1 + c2)
        else:
            return m1, c1

    def get_angle(self, ml, mr):
        s = mr - ml
        a = 1 + ml * mr

        if a == 0.0:
            return 90.0
        else:
            r = 180.0 * (1.0 - atan(s/a)/pi)
            if r>180:
                r -= 180
            return round(r,2)

    def save_result(self,mr,cr,ml,cl,fi,fname):

        t = linspace(-self.max, self.max, 2)

        x, y = self.get_xy(self.shape_atoms)
        yr = mr * t + cr
        yl = ml * t + cl

        plt.axis([-self.max - 5.0, self.max + 5.0, -0.05, self.max + 5.0])
        plt.xlabel("X")
        plt.ylabel("Y")

        plt.plot(x, y, 'yo')
        plt.plot(t, yr, 'r', label=str(mr) + "X + " + str(cr))
        plt.plot(t, yl, 'b', label=str(ml) + "X + " + str(cl))


        mx = self.get_max_atoms()
        xc = [mx[0].x, mx[1].x]
        yc = [mx[0].y, mx[1].y]
        plt.plot(xc, yc, 'go')

        an = self.get_angle(ml, mr)
        plt.text(-self.max-2, self.max+2, "$\psi=$" + str(an) + "$^{\circ}$", family="verdana")
        plt.text(-self.max-2, self.max, "$\phi_{x}=$" + str(fi) + "$^{\circ}$", family="verdana")
        plt.legend()

        plt.axes().set_aspect('equal')

        plt.savefig(fname, dpi=200)
        plt.close()

    def save_shape(self, fname):

        out = open(fname,'w')

        al, ar = self.get_max_atoms()
        out.writelines("maxleft " + str(al.x) + " " + str(al.y) + "\n")
        out.writelines("maxleft " + str(ar.x) + " " + str(ar.y) + "\n")

        for a in self.shape_atoms:
            out.writelines(str(a.x) + " " + str(a.y) + "\n")

        out.close()



    def visualize_with_angle(self, mr, cr, ml, cl, fi, show_max = False):
        t = linspace(-self.max, self.max, 2)

        x, y = self.get_xy(self.shape_atoms)
        yr = mr * t + cr
        yl = ml * t + cl

        plt.axis([-self.max - 5.0, self.max + 5.0, -0.05, self.max + 5.0])
        plt.xlabel("X")
        plt.ylabel("Y")

        plt.plot(x, y, 'yo')
        plt.plot(t, yr, 'r',label = str(mr) + "X + " + str(cr))
        plt.plot(t, yl, 'b',label = str(ml) + "X + " + str(cl))


        if show_max:
            mx = self.get_max_atoms()
            xc = [mx[0].x, mx[1].x]
            yc = [mx[0].y, mx[1].y]
            plt.plot(xc,yc,'go')

        an = self.get_angle(ml, mr)
        plt.text(-self.max - 2, self.max + 2, "$\psi=$" + str(an) + "$^{\circ}$", family="verdana")
        plt.text(-self.max - 2, self.max, "$\phi_{x}=$" + str(fi) + "$^{\circ}$", family="verdana")

        plt.axes().set_aspect('equal')

        plt.legend()

        plt.show()



    def translate(self,vec):
        for a in self.shape_atoms:
            a.translate(vec)

    def get_atoms_neighs(self, r = 3.0):
        profile_atoms = []

        for i in range(0,len(self.shape_atoms)):
            k = 0

            for j in range(i+1,len(self.shape_atoms)):
                rd = self.shape_atoms[i].dist(self.shape_atoms[j])
                if rd <= r:
                    k+=1

            profile_atoms.append((self.shape_atoms[i],k))

        return profile_atoms

    def get_atoms_profile(self, r = 3.0, neighs = 1):

        a_n = self.get_atoms_neighs(r)
        result = []

        for a in a_n:
            if a[1]<=neighs:
                result.append(a[0])

        return result

    def get_max_atoms(self):

        a_r = Atom()
        a_l = Atom()

        for a in self.shape_atoms:
            if a.x > 0 and a.y > a_r.y:
                a_r = a
            if a.x < 0 and a.y > a_l.y:
                a_l = a

        return a_l, a_r

    def visualize_profile(self, r = 3.0, neighs = 1):

        atoms = self.get_atoms_profile(r,neighs)
        for a in atoms:
            sphere(pos = (a.x, a.y, a.z), radius = a.radius, color = a.get_rgbcolor())

    def get_atoms_in_region(self,region):
        xstart = region[0]
        xfinish = region[1]
        atoms = []

        if xstart > xfinish:
            tmp = xstart
            xstart = xfinish
            xfinish = tmp

        for a in self.shape_atoms:
            if a.x >= xstart and a.x < xfinish:
                atoms.append(a)

        return atoms

    def get_avereage_r(self,N=4):
        r = 0.0

        for i in range(0,len(self.shape_atoms)):
            ds = []

            for j in range(0, len(self.shape_atoms)):
                if i!=j:
                    atom_i = self.shape_atoms[i]
                    atom_j = self.shape_atoms[j]
                    ds.append(atom_i.dist(atom_j))

            if len(ds)>=N:
                rr = 0.0
                ds.sort()

                for k in range(0,N):
                    rr += ds[k]

                r += rr / N

        return r / len(self.shape_atoms)



    def get_angle_atoms(self, region, h):
        xstart = region[0]
        xfinish = region[1]

        if xstart > xfinish:
            tmp = xstart
            xstart = xfinish
            xfinish = tmp

        xc = xstart

        sel_atoms = []

        while (xc < xfinish):
            atoms = self.get_atoms_in_region((xc,xc+h))
            if len(atoms)!=0:
                maxatom = atoms[0]
                for a in atoms:
                    if a.y > maxatom.y:
                        maxatom = a
                sel_atoms.append(maxatom)
            xc += h

        return sel_atoms











