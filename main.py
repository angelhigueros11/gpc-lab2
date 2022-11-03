# Graficas por computador
# Angel Higueros - 20460
# Lab 2 - shaders

from obj import Obj
from vector import *
import struct
from collections import namedtuple

V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])

# Métodos de escritura
def char(c): 
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(d):
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([b, g, r])


#  Herramientas
def bounding_box(*vertices):
    xs = [vertex.x for vertex in vertices]
    ys = [vertex.y for vertex in vertices]
    xs.sort()
    ys.sort()

    xMin = xs[0]
    xMax = xs[-1]
    yMin = ys[0]
    yMax = ys[-1]

    return xMin, xMax, yMin, yMax


def barycentric(a, b, c, p):
    cx, cy, cz = cross(
        V3(b.x - a.x, c.x - a.x, a.x - p.x), 
        V3(b.y - a.y, c.y - a.y, a.y - p.y)
    )


    if abs(cz) < 1:
        return -1, -1, -1 

    u = cx/cz
    v = cy/cz
    w = 1 - (u + v)

    return w, v, u

class Render(object):
    def glInit(self, filename):
        self.filename = filename
        self.framebuffer = []
        self.width = 100 
        self.height = 100
        self.zbuffer = []
        self.viewport_x = 0 
        self.viewport_y = 0 
        self.viewport_width = 100 
        self.viewport_height = 100
        self.current_color = color(255, 255, 255)
        self.vertex_color = color(200, 0, 0) # por defecto rojo
        self.active = 'OB1'

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
    

    def glViewport(self, x, y, width, height):
        self.xViewPort = x
        self.yViewPort = y
        self.viewPortWidth = width
        self.viewPortHeight = height

    def glVertex(self, x, y):

        half_size_width = self.viewport_width / 2
        half_size_height = self.viewport_height / 2

        coord_x = int((( x + 1 ) * half_size_width ))
        coord_y = int((( y + 1 ) * half_size_height ))

        self.point(coord_x, coord_y)

    def glClear(self):
        self.framebuffer = [
            [color(43,53,61) for x in range(self.width)]
            for y in range(self.height)
        ]
        self.zbuffer = [
            [-float('inf') for x in range(self.width)]
            for y in range(self.height)
        ]


    def glClearColor(self, r, g, b):
        self.clearColor(round(r * 255), round(g * 255), round(b * 255))


    def glColor(self, r, g, b):
        self.setColor(round(r * 255), round(g * 255), round(b * 255))

    def point(self, x, y, color=None):
        if 0 < x < self.width and 0 < y < self.height:
            self.framebuffer[y][x] = color or self.current_color
    
    def line(self, x0, y0, x1, y1):
        x0 = round(x0)
        y0 = round(y0)
        x1 = round(x1)
        y1 = round(y1)

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0, y0 =  y0, x0
            x1, y1 =  y1, x1

        if x0 > x1:
            x0, x1 = x1, x0 
            y0, y1 = y1, y0 

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        threshold = dx
        y =  y0

        for x in range(x0, x1 + 1):

            
            if steep:
                r.point(y, x)
            else:
                r.point(x, y)

            # offset += (dy/dx) * dx * 2
            offset += dy * 2

            if offset > threshold:
                y += 1 if y0 < y1 else  -1
                # threshold += 1 * dx * 2
                threshold += dx * 2


    def load_model(self, file, translate_factor, scale_factor):
        obj = Obj(file)

        for face in obj.faces:
            vcount = len(face)

            if vcount == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                v1 = V3(obj.vertices[f1][0],
                        obj.vertices[f1][1], 
                        obj.vertices[f1][2])
                v2 = V3(obj.vertices[f2][0],
                        obj.vertices[f2][1], 
                        obj.vertices[f2][2])
                v3 = V3(obj.vertices[f3][0],
                        obj.vertices[f3][1], 
                        obj.vertices[f3][2])

                x1 = round((v1.x * scale_factor.x) + translate_factor.x)
                y1 = round((v1.y * scale_factor.y) + translate_factor.y)
                z1 = round((v1.z * scale_factor.z) + translate_factor.z)

                x2 = round((v2.x * scale_factor.x) + translate_factor.x)
                y2 = round((v2.y * scale_factor.y) + translate_factor.y)
                z2 = round((v2.z * scale_factor.z) + translate_factor.z)

                x3 = round((v3.x * scale_factor.x) + translate_factor.x)
                y3 = round((v3.y * scale_factor.y) + translate_factor.y)
                z3 = round((v3.z * scale_factor.z) + translate_factor.z)

                self.triangle(V3(x1, y1, z1), V3(x2, y2, z2), V3(x3, y3, z3))

    def glFinish(self):
        f = open(self.filename, 'bw')

        # Pixel header
        f.write(char('B'))
        f.write(char('M'))
        # tamaño archivo = 14 header + 40  info header + resolucion
        f.write(dword(14 + 40 + self.width * self.height * 3)) 
        f.write(word(0))
        f.write(word(0))
        f.write(dword(14 + 40))

        # Info header
        f.write(dword(40)) # tamaño header
        f.write(dword(self.width)) # ancho
        f.write(dword(self.height)) # alto
        f.write(word(1)) # numero de planos (siempre 1)
        f.write(word(24)) # bits por pixel (24 - rgb)
        f.write(dword(0)) # compresion
        f.write(dword(self.width * self.height * 3)) # tamaño imagen sin header
        f.write(dword(0)) # resolucion
        f.write(dword(0)) # resolucion
        f.write(dword(0)) # resolucion
        f.write(dword(0)) # resolucion


        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[y][x])
                
    def shader(self, x, y):
        i = 0.3
        r1, g1, b1 = 226, 123, 44
        r2, g2, b2, =  70, 0, 50

        dc = 0
        
        if y >= 375 and y <= 425:
            r1, g1, b1 = 226, 123, 44
            r2, g2, b2 = 70, 0, 50
            dc = abs(y - 400)
        elif y < 450 or y > 350:
            r1, g1, b1 = 226, 123, 44
            r2, g2, b2 = 70, 0, 50
            dc = abs(y - 400)
        
        r = round(r1 + (dc / 50) * (r2 - r1) * i)
        g = round(g1 + (dc / 50) * (g2 - g1) * i)
        b = round(b1 + (dc / 50) * (b2 - b1) * i)
        
        if i > 1:
            return color(255, 255, 255)
        elif i < 0:
            return color(0, 0, 0)
        else:
            return color(r, g, b)

        
    def clearColor(self, r, g, b):
        self.framebuffer = [
            [color(r, g, b) for x in range(self.width)]
            for y in range(self.height)
        ]

    def setColor(self, r, g, b):
        self.current_color = color(r, g, b)

    def triangle(self, A, B, C):
        luz = V3(0, 0, -1)
        x_min, x_max, y_min, y_max = bounding_box(A, B, C)
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                P = V2(x, y)
                w, v, u = barycentric(A, B, C, P)
                if w < 0 or v < 0 or u < 0:
                    continue
                z = A.z * w + B.z * u + C.z * v
                colorF = self.shader(x, y)

                try:
                    if z > self.zbuffer[x][y]:
                        self.point(x, y, colorF)
                        self.zbuffer[x][y] = z
                except:
                    pass

    def transform_vertex(self, vertex, scale, translate):
        return [
            (vertex[0] * scale[0]) + translate[0],
            (vertex[1] * scale[1]) + translate[1]
        ]


# IMPLEMENTACION
r = Render()
r.glInit('lab2-shader.bmp')
r.glCreateWindow(600, 600)
r.glViewport(0, 0, 600, 600)
r.glClear()

scale_factor = V3(400, 400, 400)
translate_factor = V3(250, 250, 250)
r.load_model('objeto.obj',scale_factor, translate_factor)
r.glFinish()
