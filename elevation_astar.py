import heapq
from timeit import default_timer as timer

from utils import *
from node import Node

class AStarPathFinder:
    def __init__(self, reservations, map):
        # Current reservation table
        self.reservations = reservations

        # Elevation map
        self.map = map

        # Diagonals and cardinal direction movements allowed
        self.neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        # Only cardinal directions
        # self.neighbors = [(0,1),(0,-1),(1,0),(-1,0)]

    def find_path(self, sx, sy, fx, fy):
        '''
        Finds the least cost path from start to finish coordinates on an elevation map
        '''

        start = timer()
        nodes = [[[None for _ in range(self.map.cols)] for _ in range(self.map.rows)] for _ in range(self.reservations.time)]
        #print('Finished Instantiating node array in {}'.format(timer() - start))

        start = timer()
        for x in range(self.map.cols):
            for y in range(self.map.rows):
                for t in range(self.reservations.time):
                    z = self.map.grid[y][x]
                    nodes[t][y][x] = Node(x, y, z, t)

        #print('Finished creating nodes in {}'.format(timer() - start))

        start_time = timer()
        print('Begun pathfinding at {}'.format(start))
        open = []
        closed = set()

        start = nodes[0][sy][sx]
        end = nodes[self.reservations.time - 1][fy][fx]

        start.g = 0
        start.h = start.f = euclidean(start, end)

        heapq.heappush(open, (start.f, (sx, sy, 0)))

        while open:
            cx, cy, ct = heapq.heappop(open)[1]
            cur = nodes[ct][cy][cx]

            if cur == end:
                print('Path found in {}'.format(timer() - start_time))
                path = get_path(cur, start)
                return path

            closed.add(cur)

            neighbors = self.get_valid_neighbors(cur, nodes, start)
            print('current: {}, {}, {}'.format(cur.t, cur.x, cur.y))
            for neighbor in neighbors:
                print(neighbor.t, neighbor.x, neighbor.y)
                if not self.is_valid_move(cur, neighbor):
                    print('wasnt valid')
                    continue
                else:
                    print('was valid')
                nx, ny, nt = neighbor.x, neighbor.y, neighbor.t
                tent_g = cur.g + euclidean(cur, neighbor)

                if neighbor in closed and tent_g >= neighbor.g:
                    continue

                if tent_g < neighbor.g or (nx, ny, nt) not in [i[1] for i in open]:
                    neighbor.previous = cur
                    neighbor.g = tent_g
                    neighbor.h = euclidean(neighbor, end)
                    neighbor.f = neighbor.g + neighbor.h
                    heapq.heappush(open, (neighbor.f, (nx, ny, nt)))

        print('No solution found in {} time steps'.format(self.reservations.time))
        return None

    def get_valid_neighbors(self, cur, nodes, start):
        '''
        Returns a list of valid neighboring nodes
        '''

        t = cur.t + 1
        neighbors = []
        if t < self.reservations.time:
            for dy, dx in self.neighbors:
                x = cur.x + dx
                y = cur.y + dy

                # Check out of bounds neighbor
                if x < 0 or y < 0 or x >= self.map.cols or y >= self.map.rows:
                    continue

                # Check availability in reservation table
                if not self.reservations.table[t][y][x]:
                    continue

                neighbor = nodes[t][y][x]

                # Check if slope is too great between current and neighboring node
                if (neighbor.z - cur.z) > 2:
                    continue

                # Prevent backward move
                if cur != start and neighbor == nodes[t][cur.previous.y][cur.previous.x]:
                    continue

                neighbors.append(neighbor)

            # Add current location as a possible wait step
            neighbors.append(nodes[t][cur.y][cur.x])

        return neighbors

    def is_valid_move(self, cur, neighbor):
        '''
        Checks a move's edge cases such as moving in between mountains or through other agents
        '''

        dx = abs(cur.x - neighbor.x)
        dy = abs(cur.y - neighbor.y)

        # Double check reservation table
        if not self.reservations.table[neighbor.t][neighbor.y][neighbor.x]:
            print('tried to move directly onto something..')
            return False

        # Prevent agents moving through one another
        if self.reservations.is_blocked(neighbor.x, neighbor.y, cur.t) and self.reservations.is_blocked(cur.x, cur.y, neighbor.t):
            #print('caught linear collision')
            return False

        # Diagonal move
        if dx == 1 and dy == 1:
            # Check for mountains or craters adjacent to diagonal move
            if abs((self.map.grid[cur.y][neighbor.x] - self.map.grid[cur.y][cur.x]) > 2 or abs(self.map.grid[neighbor.y][cur.x] - self.map.grid[cur.y][cur.x]) > 2 or

            # Prevent agents moving through one another diagonally
            (self.reservations.is_blocked(neighbor.x, neighbor.y, cur.t) and self.reservations.is_blocked(cur.x, neighbor.y, neighbor.t)) or
            (self.reservations.is_blocked(neighbor.x, cur.y, neighbor.t) and self.reservations.is_blocked(cur.x, neighbor.y, cur.t))):
               # print('caught diagonal collision')
                return False



        return True