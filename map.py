import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import noise
import random as rand
import os
from node import Node
import cv2

from utils import *

def random_map(cols, rows):
    '''
    Generates a random elevation map using Perlin noise
    '''
    z_grid = np.empty((rows, cols))

    y_cnt = rand.random()
    for i in range(rows):
        x_cnt = 0.0
        for j in range(cols):
            z_grid[i][j] = (noise.pnoise2(x_cnt, y_cnt, octaves=2, persistence=0.5, \
                                          lacunarity=2.0, repeatx=100, repeaty=100) * 30)

            x_cnt += 0.03
        y_cnt += 0.03

    return z_grid

class ElevationMap:
    '''
    Stores a grid of Nodes as well as the elevation map being used
    '''
    def __init__(self, w, h, rows, cols, initial_grid = None):
        self.w = w
        self.h = h
        self.rows = rows
        self.cols = cols

        self.grid = None

        # Use given elevation map or create random
        if initial_grid is not None:
            if rows != np.array(initial_grid).shape[0] or cols != np.array(initial_grid).shape[1]:
                raise ValueError('Shape of initial grid does not match given number of rows and columns.')

            self.grid = initial_grid
        else:
            self.grid = random_map(cols, rows)

    def animate(self, agents, paths, vid_path, t):
        for path in paths.values():
            print(path)

        x = np.arange(0, self.cols, 1)
        y = np.arange(0, self.rows, 1)
        x_grid, y_grid = np.meshgrid(x, y)

        colors = ["#" + ''.join([rand.choice('0123456789ABCDEF') for j in range(6)])
                 for i in range(len(agents))]

        i = 0
        files = []
        while i < t:
            fig = plt.figure()
            ax = plt.axes(projection='3d')
            ax.plot_surface(x_grid, y_grid, self.grid, cmap='viridis', edgecolor='None', alpha=0.4)

            for k, path in enumerate(paths.values()):
                if path:
                    ax.scatter([path[i][0]], [path[i][1]], self.grid[path[i][1]][path[i][0]], s=100, color=colors[k], cmap='RdGy')

            ax.view_init(75, 270)
            file = str(i) + '.jpg'
            files.append(file)
            plt.savefig(os.path.join(vid_path, file))
            plt.close(fig)
            i += 1

        print('-> Building the simulation video')
        imgs = [cv2.imread(os.path.join(vid_path, file)) for file in files]
        height, width = imgs[0].shape[0:2]

        fps = 1
        orig_video = cv2.VideoWriter(os.path.join(os.getcwd(), 'simulation.avi'),
                                     cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, (width, height))
        for image in imgs:
            orig_video.write(image)

        cv2.destroyAllWindows()
        orig_video.release()
        print('-> Done building simulation')

    def show_grid(self, agents, paths):
        '''
        Displays the elevation map in 2d and 3d
        '''

        # Creating 2D plot
        for agent in agents:
            plt.scatter([agent.sx], [agent.sy], s=100, color='green')
            plt.scatter([agent.fx], [agent.fy], s=100, color='red')

            path = paths[agent.num]
            if path:
                xs = [node[0] for node in path]
                ys = [node[1] for node in path]
                plt.plot(xs, ys, linewidth=3)

        plt.imshow(self.grid, origin='lower', cmap='RdGy')
        plt.colorbar()
        plt.axis(aspect='image');

        for (j, i), label in np.ndenumerate(self.grid):
            plt.text(i, j, np.round(label, 2), ha='center', va='center', fontsize=8)

        plt.show()

        # Creating 3D plot
        x = np.arange(0, self.cols, 1)
        y = np.arange(0, self.rows, 1)
        x_grid, y_grid = np.meshgrid(x, y)

        ax = plt.axes(projection='3d')
        ax.plot_surface(x_grid, y_grid, self.grid, cmap='viridis', edgecolor='None', alpha=0.4)

        for agent in agents:
            ax.scatter([agent.sx], [agent.sy], self.grid[agent.sy][agent.sx], s=100, color='green')
            ax.scatter([agent.fx], [agent.fy], self.grid[agent.fy][agent.fx], s=100, color='red')

            path = paths[agent.num]
            if path:
                xs = [node[0] for node in path]
                ys = [node[1] for node in path]
                zs = [self.grid[y][x] for x, y, t in path]
                plt.plot(xs, ys, zs, linewidth=2)

        ax.view_init(75, 270)
        plt.show()
