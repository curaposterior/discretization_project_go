import math
import random
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def circumcenter(a, b, c):
    ad = a[0] * a[0] + a[1] * a[1]
    bd = b[0] * b[0] + b[1] * b[1]
    cd = c[0] * c[0] + c[1] * c[1]
    D = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
    return (1 / D * (ad * (b[1] - c[1]) + bd * (c[1] - a[1]) + cd * (a[1] - b[1])),
            1 / D * (ad * (c[0] - b[0]) + bd * (a[0] - c[0]) + cd * (b[0] - a[0])))

def is_line_equal(line1, line2):
    if (line1[0] == line2[0] and line1[1] == line2[1]) or (line1[0] == line2[1] and line1[1] == line2[0]):
        return True
    return False

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.edges = [[self.a, self.b],
                      [self.b, self.c],
                      [self.c, self.a]]
        self.circumcenter = circumcenter(a, b, c)

    def has_vertex(self, point):
        if self.a == point or self.b == point or self.c == point:
            return True
        return False

    def is_point_in_circumcircle(self, point):
        if distance(self.a, self.circumcenter) > distance(point, self.circumcenter):
            return True
        return False

    def __str__(self):
        return f"T[{self.a}, {self.b}, {self.c}]"

    def __repr__(self):
        return f"T[{self.a}, {self.b}, {self.c}]"

def bowyer_watson(points, width, height):
    triangulation = []
    superTriangleA = (-100, -100)
    superTriangleB = (2 * width + 100, -100)
    superTriangleC = (-100, 2 * height + 100)

    superTriangle = Triangle(superTriangleA, superTriangleB, superTriangleC)
    triangulation.append(superTriangle)

    onSuper = lambda triangle: triangle.has_vertex(superTriangleA) or triangle.has_vertex(superTriangleB) or triangle.has_vertex(superTriangleC)

    for point in points:
        badTriangles = []
        for triangle in triangulation:
            if triangle.is_point_in_circumcircle(point):
                badTriangles.append(triangle)

        polygon = []
        for triangle in badTriangles:
            for triangleEdge in triangle.edges:
                isShared = False
                for other in badTriangles:
                    if triangle == other:
                        continue
                    for otherEdge in other.edges:
                        if is_line_equal(triangleEdge, otherEdge):
                            isShared = True
                if not isShared:
                    polygon.append(triangleEdge)

        for badTriangle in badTriangles:
            triangulation.remove(badTriangle)

        for edge in polygon:
            newTriangle = Triangle(edge[0], edge[1], point)
            triangulation.append(newTriangle)

    to_be_removed = []
    for triangle in triangulation:
        if onSuper(triangle):
            to_be_removed.append(triangle)
    for triangle in to_be_removed:
        triangulation.remove(triangle)

    return triangulation

def laplacian_smoothing(points, iterations):
    pass

def find_neighbours(points, point):
    pass

def transform_triangles(points, triangles):
    new_tri = []
    for tri in triangles:
        new_tri.append((points.index(tri.a),
                        points.index(tri.b),
                        points.index(tri.c)))
    return new_tri

def plot(points, delaunay):
    for tri in delaunay:
        plt.plot([tri.a[0], tri.b[0], tri.c[0]], [tri.a[1], tri.b[1], tri.c[1]], '-k')

    plt.scatter([x[0] for x in points], [x[1] for x in points], s=0.8, c='r')
    

    plt.show()

def save_mesh(points, triangles):
    triangles = transform_triangles(points, triangles)
    with open('mesh.txt', 'w') as f:
        f.write("Nodes\n")
        for i, point in enumerate(points):
            f.write(f"{i} {point[0]} {point[1]}\n")
        f.write("Elements")
        for j, element in enumerate(triangles):
            f.write(f"{j} {element[0]} {element[1]} {element[2]}\n")

def read_image(file_path):
    image = Image.open(file_path)
    image = image.convert("RGB")
    width, height = image.size
    gap = 50
    points = []
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            if r == 0 and g == 0 and b == 0:  # Assuming black pixels represent the points
                points.append((x, y))

    for y in range(0, height, gap):
        for x in range(0, width, gap):
            r, g, b = image.getpixel((x, y))
            if (x,y) not in points:
                if r == 255 and g == 255 and b == 255:
                    points.append((x,y))

    return width, height, points

# Wczytaj obrazek
image_path = "test_2.png"  # Ścieżka do obrazka PNG lub JPG
width, height, points = read_image(image_path)

amount = len(points)

delaunay = bowyer_watson(points, width, height)
plot(points, delaunay)
save_mesh(points, delaunay)
# from scipy.spatial import Delaunay
# tri = Delaunay(points)
# plt.triplot([x[0] for x in points], [x[1] for x in points], tri.simplices)
# plt.plot([x[0] for x in points], [x[1] for x in points], '.r')
# plt.show()