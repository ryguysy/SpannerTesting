class TreeNode:
    def __init__(self, value, nodes):
        self.value = value
        self.nodes = nodes
        self.left = None
        self.right = None

class BoundingBox:
    def __init__(self, min_corner, max_corner):
        self.min_corner = min_corner
        self.max_corner = max_corner
        self.width = max_corner[0] - min_corner[0]
        self.height = max_corner[1] - min_corner[1]
        self.center = ((min_corner[0] + max_corner[0]) / 2, (min_corner[1] + max_corner[1]) / 2)
        self.radius = math.sqrt(self.width**2 + self.height**2) / 2
        self.lmax = max(self.width, self.height)