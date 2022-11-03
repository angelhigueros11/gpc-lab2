from collections import namedtuple

V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])


class V3_(object):
    def __init__(self, x, y, z = 0):
            self.x = x
            self.y = y
            self.z = z

    def round(self):
        self.x = round(self.x)
        self.y = round(self.y)
        self.z = round(self.z)

    def __add__(self, other):
        return V3(
                self.x + other.x,
                self.y + other.y,
                self.z + other.z,
            )
    
    def __sub__(self, other):
        return V3(
                self.x - other.x,
                self.y - other.y,
                self.z - other.z,
            )
    
    def __mul__(self, other):
        if type(other) == int or  type(other) == float:
            return V3(
                    self.x * other, 
                    self.y * other,
                    self.z * other,
                )
        
        return V3(
            self.y * other.z - self.z * self.y,
            self.z * other.x - self.x * self.z,
            self.x * other.y - self.y * self.x,
        )

    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def __matmul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def norm(self):
        try:
            return self * (1 / self.length())
        except:
            return self * (1 / self.length())


    def __repr__(self):
        return "V3(%s, %s, %s)" % (self.x, self.y, self.z)

def sum(x, y):
    return V3(
        x.x + y.x,
        x.y + y.y,
        x.z + y.z)


def sub(x, y):
    return V3(
        x.x - y.x,
        x.y - y.y,
        x.z - y.z
    )


def mul(x, k):
    return V3(
        x.x * k,
        x.y * k,
        x.z * k
    )


def dot(x, y):
    return x.x * y.x + x.y * y.y + x.z * y.z


def length(x):
    return (x.x ** 2 + x.y ** 2 + x.z**2) **0.5


def norm(x):
    l = length(x)
    if not l:
        return V3(0, 0, 0)

    return V3( x.x / l,
               x.y / l,
               x.z / l)

def cross(u, w):
    return V3(
        u.y * w.z - u.z * w.y,
        u.z * w.x - u.x * w.z,
        u.x * w.y - u.y * w.x,
    )



