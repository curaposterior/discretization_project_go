# basic point quadtree
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Node:
    def __init__(self, x0, y0, w, h):
        self.x0 = x0
        self.y0 = y0
        self.width = w
        self.height = h
        self.type_id = 0
        self.children = []

    def show_data(self):
        print(f"x0 = {self.x0}, y0 = {self.y0}, width = {self.width}, height = {self.height}")

    def get_data(self):
        return self.x0, self.y0, self.width, self.height, self.type_id

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def count_black_white(self, data):
        white, black = 0, 0
        for j in range(self.y0, self.y0 + self.height):
            for i in range(self.x0, self.x0 + self.width):
                if data[i, j] == 0:
                    black += 1
                else:
                    white += 1
        return white


def recursive_subdivide(node, size_threshold, img):
    if node.count_black_white(img) <= 1:
        node.type_id = 1
        return

    if node.get_width() <= size_threshold or node.get_height() <= size_threshold:
        return
    w_1 = int(math.floor(node.width / 2))
    w_2 = int(math.ceil(node.width / 2))
    h_1 = int(math.floor(node.height / 2))
    h_2 = int(math.ceil(node.height / 2))

    x1 = Node(node.x0, node.y0, w_1, h_1)  # top left
    recursive_subdivide(x1, size_threshold, img)

    x2 = Node(node.x0, node.y0 + h_1, w_1, h_2)  # btm left
    recursive_subdivide(x2, size_threshold, img)

    x3 = Node(node.x0 + w_1, node.y0, w_2, h_1)  # top right
    recursive_subdivide(x3, size_threshold, img)

    x4 = Node(node.x0 + w_1, node.y0 + h_1, w_2, h_2)  # btm right
    recursive_subdivide(x4, size_threshold, img)

    node.children = [x1, x2, x3, x4]


def get_children(node):
    if not node.children:
        return [node]
    else:
        children = []
        for child in node.children:
            children += get_children(child)
    return children
