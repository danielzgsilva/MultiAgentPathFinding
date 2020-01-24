import numpy as np
import matplotlib.pyplot as plt

def euclidean(a, b):
    '''
    Returns the 3D euclidean distance between 2 nodes
    '''
    return np.round(np.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2 + (b.z - a.z) ** 2), 2)


def get_path(cur, start):
    '''
    Backtracks the path starting at the current node using the nodes previous pointers
    '''
    path = []
    print('-> backtracking')
    while cur != start:
        print('-> ', cur.t, cur.x, cur.y)
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