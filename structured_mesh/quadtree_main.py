import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from quadtree import Node, recursive_subdivide, get_children


class QTree:
    def __init__(self, k, img_width, img_height, img):
        self.threshold = k
        self.img = img
        self.root = Node(0, 0, img_width, img_height)

    def get_points(self):
        return self.img[self.root.x0:self.root.x0 + self.root.get_width(),
               self.root.y0:self.root.y0 + self.root.get_height()]

    def save_elements(self):
        children = self.return_children()
        with open('elements.txt', 'w') as f:
            for count, child in enumerate(children):
                x0, y0, width, height, type_id = child.get_data()
                f.write(f"Element {count} node_1 = {x0},{y0};"
                        f"node_2 = {x0 + width}, {y0};"
                        f"node_3 = {x0},{y0 + height};"
                        f"node_4 = {x0 + width},{y0 + height};"
                        f"Type = {type_id}\n")

    def subdivide(self):
        recursive_subdivide(self.root, self.threshold, self.img)

    def return_children(self):
        return get_children(self.root)

    def graph(self):
        im = Image.open("test_image.jpg")
        plt.imshow(im)
        plt.title("Quadtree")

        ax = plt.gca()

        c = get_children(self.root)
        print("Number of segments: %d" % len(c))
        areas = set()
        for el in c:
            areas.add(el.width * el.height)
        print("Minimum segment area: %.3f units" % min(areas))
        for n in c:
            ax.add_patch(patches.Rectangle((n.x0, n.y0), n.width, n.height, edgecolor='r', fill=False))

        plt.savefig('Structured_mesh.png')
        plt.show()
        return


img = Image.open("test_image.jpg")
data = img.load()

k = int(input("Podaj dokladnosc siatki - mniejsza liczba dokladniesza siatka\n"))

tree = QTree(k, img.size[0], img.size[1], data)
tree.subdivide()
tree.save_elements()
tree.graph()
