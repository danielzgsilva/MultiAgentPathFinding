import matplotlib
import matplotlib.pyplot as plt
import random as rand
import cv2 as cv
import numpy as np
import heapq
import time

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wall = False if rand.random() > 0.3 else True
        self.g = float('inf')
        self.h = None
        self.f = None
        self.previous = None

    def get_valid_neighbors(self, map):
        neighbors = []
        for dy, dx in map.neighbors:
            x = self.x + dx
            y = self.y + dy

            if x < 0 or y < 0 or x >= map.cols or y >= map.rows:
                continue

            neighbor = map.grid[y][x]
            if not neighbor.wall:
                neighbors.append(neighbor)

        return neighbors

class Map:
    def __init__(self, w, h, rows, cols, initial_grid = False):
        self.w = w
        self.h = h
        self.rows = rows
        self.cols = cols

        self.grid = []

        for j in range(rows):
            row = [Node(i, j) for i in range(cols)]
            self.grid.append(row)

        if initial_grid is not None:
            for j in range(initial_grid.shape[0]):
                for i in range(initial_grid.shape[1]):
                    if initial_grid[j][i] == 1:
                        self.grid[j][i].wall = True
                    else:
                        self.grid[j][i].wall = False

        self.neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
        #self.neighbors = [(0,1),(0,-1),(1,0),(-1,0)]

        self.map = np.full((h,w,3), 255, np.uint8)

        for i in range(rows):
            for j in range(cols):
                if self.grid[i][j].wall and (i, j) != (0,0) and (i, j) != (rows-1, cols-1):
                    self.fill_cell(j, i, (0,0,0))
                else:
                    self.draw_cell(j,i)

    def fill_cell(self, i, j, color):
        cv.rectangle(self.map, (i * (self.w // self.cols), j * (self.h // self.rows)),
                     ((i + 1) * (self.w // self.cols), (j + 1) * (self.h // self.rows)), color, -1)

    def draw_cell(self, i, j):
        cv.rectangle(self.map, (i * (self.w // self.cols), j * (self.h // self.rows)),
                     ((i + 1) * (self.w // self.cols), (j + 1) * (self.h // self.rows)), (0,0,0), 1)

    def draw_symbol(self, i, j, color):
        cv.circle(self.map, (int(i * (self.w / self.cols) + 0.5*(self.w / self.cols)),
                             int(j * (self.h // self.rows) + 0.5*(self.h // self.rows))), 8, color, -1)

    def prime_map(self, start, end):
        map.draw_symbol(start.x, start.y, (0, 255, 0))
        map.draw_symbol(end.x, end.y, (255, 0, 0))
        start.wall = False
        end.wall = False

    def show_grid(self, open = [], closed = [], start = None, end = None):
        for cell in open:
            if cell[1] != (start.x, start.y) and cell[1] != (end.x, end.y) and start and end:
                self.fill_cell(cell[1][0], cell[1][1], (255, 0, 0))
        for cell in closed:
            if cell != (start.x, start.y) and cell != (end.x, end.y) and start and end:
                self.fill_cell(cell[0], cell[1], (0, 255, 0))

        plt.axis('off')
        plt.imshow(self.map)
        plt.show()
        #cv.imshow('test', self.map)

    def draw_path(self, path):
        cell_w = (map.w / map.cols)
        cell_h = (map.h / map.rows)

        #for i, j in path:
         #   map.fill_cell(i, j, (0, 0, 255))
        i = 0
        j = i+1

        while j < len(path):
            cv.line(self.map, (int(path[i][0] * cell_w + 0.5 * cell_w), int(path[i][1] * cell_h + 0.5 * cell_h)),
                    (int(path[j][0] * cell_w + 0.5 * cell_w), int(path[j][1] * cell_h + 0.5 * cell_h)), (252, 15, 192), 4)
            i += 1
            j = i + 1

        map.show_grid()

    def is_valid_move(self, cur, neighbor):
        # Diagonal move not possible if one cell is blocked...
        dx = abs(cur[0] - neighbor[0])
        dy = abs(cur[1] - neighbor[1])

        # Diagonal move
        if dx == 1 and dy == 1:
            if self.grid[neighbor[1]][neighbor[0]].wall or self.grid[cur[1]][cur[0]].wall \
                    or self.grid[cur[1]][neighbor[0]].wall or self.grid[neighbor[1]][cur[0]].wall:
                return False

        return True
def euclidean(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def get_path(cur, previous, sx, sy):
    path = []
    while cur in previous:
        path.append(cur)
        cur = previous[cur]

    path.append((sx, sy))
    map.draw_path(path)
    return path

def a_star(map, sx, sy, fx, fy):
    open = []
    closed = set()
    previous = {}

    start = map.grid[sy][sx]
    end = map.grid[fy][fx]

    map.prime_map(start, end)
    map.show_grid(open, closed, start, end)

    start.g = 0
    start.h = start.f = euclidean((sx, sy), (fx, fy))
    heapq.heappush(open, (start.f, (sx, sy)))

    while open:
        cur = heapq.heappop(open)[1]
        cur_node = map.grid[cur[1]][cur[0]]

        if cur_node == end:
            print('Found Path!')
            path = get_path(cur, previous, sx, sy)
            map.draw_path(path)
            return path

        closed.add(cur)

        neighbors = cur_node.get_valid_neighbors(map)
        for neighbor in neighbors:
            neighbor_coord = (neighbor.x, neighbor.y)
            if not map.is_valid_move(cur, neighbor_coord):
                continue

            tent_g = cur_node.g + euclidean(cur, neighbor_coord)

            if neighbor_coord in closed and tent_g >= neighbor.g:
                continue

            if tent_g < neighbor.g or neighbor_coord not in [i[1] for i in open]:
                previous[neighbor_coord] = cur
                neighbor.g = tent_g
                neighbor.h = euclidean(neighbor_coord, (fx, fy))
                neighbor.f = neighbor.g + neighbor.h
                heapq.heappush(open, (neighbor.f, neighbor_coord))

        '''path = get_path(cur, previous, sx, sy)
        map.draw_path(path)
        map.show_grid()
        time.sleep(1)'''

    print('No Solution')
    return None

if __name__ == "__main__":
    test_grid = np.array([
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

    map = Map(w = 400, h = 400, rows = 20, cols = 20, initial_grid = None)

    path = a_star(map, 0, 0, map.cols-1, map.rows-1)