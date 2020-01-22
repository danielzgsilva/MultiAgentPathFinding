class Node:
    def __init__(self, x, y, z, t):
        self.x = x
        self.y = y
        self.z = z
        self.t = t
        self.g = float('inf')
        self.h = None
        self.f = None
        self.previous = None