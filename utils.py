import numpy as np
import matplotlib.pyplot as plt
import noise
from opensimplex import OpenSimplex
import random as rand

def euclidean(a, b):
    '''
    Returns the 3D euclidean distance between 2 nodes
    '''
    return np.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2 + (b.z - a.z) ** 2)

def coords(s):
    try:
        x, y = map(int, s.split(','))
        return x, y
    except:
        raise TypeError("Coordinates must be x,y")


def get_path(cur, start):
    '''
    Backtracks the path starting at the current node using the nodes previous pointers
    '''
    path = []
    while cur != start:
        path.append((cur.x, cur.y, cur.t))
        cur = cur.previous

        if cur is None:
            raise AssertionError('Unable to backtrack to start node.')

    path.append((start.x, start.y, 0))
    return path[::-1]


def get_cmap(n, name='RdGy'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''

    return plt.cm.get_cmap(name, n)


def simple_noise(x, y):
    return (noise.pnoise2(x, y, octaves=2, persistence=0.5,
                   lacunarity=2.0, repeatx=100, repeaty=100) * 30)


def simple_map(cols, rows):
    '''
    Generates a random elevation map using Perlin noise
    '''
    z_grid = np.empty((rows, cols))

    y_cnt = rand.random()
    for i in range(rows):
        x_cnt = 0.0
        for j in range(cols):
            z_grid[i][j] = simple_noise(x_cnt, y_cnt)

            x_cnt += 0.03
        y_cnt += 0.03

    return z_grid


def simple_curve(value):
    start = 0.4
    end = 0.6
    if value < start:
        return 0.0
    if value > end:
        return 1.0
    return (value - start) * (1 / (end - start))


def interpolate(a, b, weight):
    new_weight = simple_curve(weight)

    return a * (1 - new_weight) + b * new_weight


def simple_scurve():
    tmp = OpenSimplex(int(rand.random() * 10000))

    def noise(x, y):
        noise = (tmp.noise2d(x/5.0, y/5.0) + 1) / 2.0

        return interpolate(0.0, 1.0, noise) * 10.0

    return noise


def plains():
    tmp = OpenSimplex(int(rand.random() * 10000))

    def noise(x, y):
        value = (tmp.noise2d(x/3.0, y/3.0) + 1) / 2.0

        value = value**0.25

        value = value - 0.6

        if value < 0:
            value = 0

        return value * 6.0

    return noise


def mountains():
    tmp = OpenSimplex(int(rand.random() * 10000))

    def noise(x, y):
        value = (tmp.noise2d(x*2.0, y) + 1) / 2.0

        value = value

        return value * 10.0

    return noise


def combined():
    m_values = mountains()
    p_values = plains()
    weights = simple_scurve()

    def noise(x, y):
        m = m_values(x, y)
        p = p_values(x, y)
        w = weights(x, y) / 10.0

        return (p * w) + (m * (1 - w))

    return noise

def elevation_map(cols, rows, map_type):
    z_grid = np.empty((rows, cols))
    func = None

    if map_type == 'mountains':
        func = mountains()
    elif map_type == 'plains':
        func = plains()
    elif map_type == 'canyons':
        func = simple_scurve()
    elif map_type == 'combined':
        func = combined()
    else:
        raise ValueError('Map type not supported.')

    for x in range(cols):
        for y in range(rows):
            z_grid[y][x] = func(x, y)

    return z_grid