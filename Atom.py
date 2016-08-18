from math import sqrt, cos, sin

class Quaternion(object):

    def __init__(self,w=0.0,x=0.0,y=0.0,z=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Quaternion(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Quaternion(self.w - other.w, self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Quaternion(self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z,
                              other.w*self.x + self.w*other.x - other.y*self.z + self.y*other.z,
                              other.w*self.y + self.w*other.y + other.x*self.z - self.x*other.z,
                             -other.x*self.y + self.x*other.y + other.w*self.z + self.w*other.z)

        if isinstance(other,float) or isinstance(other,int):
            return Quaternion(self.w * other, self.x * other, self.y * other, self.z * other)

        if isinstance(other,Atom):
            q = Quaternion(x = other.x, y = other.y, z = other.z)
            return self*q

    def __str__(self):
        return '{u.w} {u.x} {u.y} {u.z}'.format(u=self)

    def get_conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def get_norm(self):
        return sqrt(self.w*self.w + self.x*self.x + self.y*self.y + self.y*self.y)

    def get_reverse(self):
        a = 1.0/self.get_norm()
        res = self.get_conjugate() * a
        return res



class Atom(object):

    def __init__(self, x = 0.0, y = 0.0, z = 0.0, symbol = 'Au', radius = 1.0, color = '0x0000FF', sel = 'y'):
        self.x = x
        self.y = y
        self.z = z
        self.symbol = symbol
        self.radius = radius
        self.color = color
        self.sel = sel

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Atom(self.x + other.x,self.y + other.y, self.z + other.z,'')

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Atom(self.x - other.x, self.y - other.y, self.z - other.z, '')

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return self.x * other.x + self.y * other.y + self.z * other.z

        if isinstance(other, float) or isinstance(other, int):
            return Atom(self.x*other, self.y*other, self.z*other)

        if isinstance(other, Quaternion):
            q = Quaternion(0.0, self.x, self.y, self.z)
            return q * other

    def __str__(self):
        return '{u.symbol} {u.x} {u.y} {u.z} {u.radius} {u.color}'.format(u=self)

    def dist(self,atom):
        return sqrt((atom.x-self.x)*(atom.x-self.x) + (atom.y-self.y)*(atom.y-self.y) + (atom.z-self.z)*(atom.z-self.z))

    def translate(self,vec):
        if isinstance(vec,tuple):
            self.x += vec[0]
            self.y += vec[1]
            self.z += vec[2]

    def rotate(self, fi, along):
        if isinstance(along,tuple):
            sinn = sin(fi*0.5)
            q = Quaternion(cos(fi*0.5), along[0] * sinn, along[1] * sinn, along[2] * sinn)
            a = Quaternion(x = self.x, y = self.y, z = self.z)
            r = q * a * q.get_reverse()
            self.x = r.x
            self.y = r.y
            self.z = r.z

    def get_rgbcolor(self):

        if len(self.color)==8:
            rs = self.color[6:8]
            gs = self.color[4:6]
            bs = self.color[2:4]
            r = int(rs,16)/255.0
            g = int(gs,16)/255.0
            b = int(bs,16)/255.0
            return r, g, b
        else:
            return 0.0, 0.0, 1.0

    def get_bgrcolor(self):

        if len(self.color)==8:
            rs = self.color[6:8]
            gs = self.color[4:6]
            bs = self.color[2:4]
            r = int(rs,16)/255.0
            g = int(gs,16)/255.0
            b = int(bs,16)/255.0
            return b, g, r
        else:
            return 1.0, 0.0, 0.0






