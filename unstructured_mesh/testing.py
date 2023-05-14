from PIL import Image
from random import randint
import math

import numpy as np
from numpy import asarray

import matplotlib.pyplot as plt


def vecDiff2D(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])


def vecDiff3D(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])


def vecCross2D(p1, p2, p3):
    """
    returns the cross product between p1->p2 vector and p1->p3 vector
    """
    v1 = vecDiff2D(p2, p1) # p2 - p1
    v2 = vecDiff2D(p3, p1) # p3 - p1
    return v1[0] * v2[1] - v1[1] * v2[0]


def planePoint(p):
    """
    converts (x, y) to a point on a 3d surface (x, y, x^2 + y^2)
    """
    return (p[0], p[1], p[0]*p[0] +p[1]*p[1])


def ccw(p1, p2, p3):
    """
    returns true iff p1->p2 vector and p1->p3 vector are in counter-clockwise position
    """
    return vecCross2D(p1, p2, p3) > 0


def isInCircum(p, p1, p2, p3):
    """
    returns true iff p is in the circumcircle of triangle (p1,p2,p3)
    """
    p = planePoint(p)
    p1 = planePoint(p1)
    p2 = planePoint(p2)
    p3 = planePoint(p3)

    v1 = vecDiff3D(p1, p) # p1 - p
    v2 = vecDiff3D(p2, p) # p2 - p
    v3 = vecDiff3D(p3, p) # p3 - p

    # the volume of tetrahedron (p, p1, p2, p3) where each points are the "plane points".
    # iff p is outside, planePoint(p) is below the plane containing p1, p2, p3 on 3d space
    # and therefore the determinent positive, given that p1, p2, p3 are in counter-clockwise order.
    det = v1[0] * (v2[1] * v3[2] - v2[2] * v3[1]) - v1[1] * (v2[0] * v3[2] - v2[2] * v3[0]) + v1[2] * (v2[0] * v3[1] - v2[1] * v3[0])

    if ccw(p1, p2, p3):
        return det > 0
    else:
        return det < 0


def validate(triangles):
    for t in triangles:
        # check if the triangulation has a triangle that contains another point in its circumcircle
        for p in pointList:
            if p not in t and isInCircum(p, t[0], t[1], t[2]):
                return False
    return True


def bowyer_watson(pointList):
    """
    returns the Delaunay Triangulation using Bowyer-Watson algorithm
    """
    triangles = [] # the resulting triangle mesh
    
    # insert super triangle
    bignum = math.inf
    supertriangle = ((-bignum, -bignum), (bignum, -bignum), (0, bignum))
    triangles.append(supertriangle)

    # incrementally insert point and rebowyer_watson 'bad triangles'
    for p in pointList:
        badTriangles = []
        badEdges = set()
        for t in triangles:
            # find all triangles where its circumcircle contains the new point p.
            # the 'bad triangles' will form a star-shaped polygon.
            if isInCircum(p, t[0], t[1], t[2]):
                badTriangles.append(t)
                # keep track of the star-shaped polygon's boundary.
                # since each edge is shared by two triangles,
                # duplicate insertion implies that this edge is not on the boundary.
                edges = [(t[0], t[1]), (t[1], t[0]), (t[1], t[2]), (t[2], t[1]), (t[0], t[2]), (t[2], t[0])] # three edges in both directions
                for i in range(0, 3):
                    # since the order of points in an edge is arbitrary, we need to search for either p1->p2 or p2->p1
                    edgeAndReverse = {edges[i*2], edges[i*2+1]}
                    if len(badEdges.intersection(edgeAndReverse)) == 0:
                        badEdges.add(edges[i*2])
                    else:
                        badEdges = badEdges.difference(edgeAndReverse)

        # now remove bad triangles to create star-shaped polygon hole
        for t in badTriangles:
            triangles.remove(t)
        
        # insert new triangulation for the hole
        for edge in badEdges:
            triangles.append((edge[0], edge[1], p))

    # after inserting all points, remove triangles connected to the supertriangle
    badTriangles = []
    for t in triangles:
        # check if any of the three vertices are shared with the supertriangle
        for i in range(0, 3):
            if t[i] in supertriangle:
                badTriangles.append(t)
                break
    for t in badTriangles:
        triangles.remove(t)

    # confirm that we don't have any bad triangles
    if validate(triangles) == False:
        raise RuntimeError('Invalid triangulation!!!')

    return triangles



def read_image_as_matrix(fname: str):
    '''
    255 value represents white color,
    0 represents black
    '''
    return asarray(Image.open(fname))

def get_black_pixels(matrix):
    black_pixels = np.where(matrix == 0)
    return list(zip(black_pixels[0], black_pixels[1]))

# pointList = []

def read_image_as_pointlist(filename):
    img = Image.open('test.png')

    # Convert the image to a numpy array
    img_array = np.asarray(img)

    # Get the indices of black pixels in the image
    black_pixels = np.where(img_array == 0)
    return list(zip(black_pixels[1], black_pixels[0]))


def generate_points(numberOfPoints: int, left: int, right: int): #generowanie punktow
    return [(randint(left, right), randint(left, right)) for _ in range(numberOfPoints)]

# pointList = generate_points(30, 0, 30)
# X, Y = [x[0] for x in pointList], [y[1] for y in pointList]

img = Image.open('test.png')

# Convert the image to a numpy array
img_array = np.asarray(img)

# Get the indices of black pixels in the image
black_pixels = np.where(img_array == 0)

# Create a list of points from the indices of black pixels
pointList = list(zip(black_pixels[1], black_pixels[0]))
X, Y = [x[0] for x in pointList], [y[1] for y in pointList]

tr = bowyer_watson(pointList=pointList)
triangles = []

# print(pointList)

for t in tr:
    # print(t)
    triangles.append((pointList.index(t[0]),
                     pointList.index(t[1]),
                     pointList.index(t[2])))
# print(triangles)

# fig, ax = plt.subplots(figsize=(12,12))
# plt.ion()
plt.imshow(img, cmap='Oranges_r')
# plt.scatter([x[0] for x in pointList], [y[1] for y in pointList], s=0.5)
plt.triplot(X, Y, triangles)
plt.show()