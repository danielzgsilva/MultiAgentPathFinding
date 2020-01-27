import numpy as np
import os
from node import Node

from utils import *

class ElevationMap:
    '''
    Stores a grid of Nodes as well as the elevation map being used
    '''
    def __init__(self, rows, cols, map_type, initial_grid = None):
        self.rows = rows
        self.cols = cols
        self.map_type = map_type
        self.grid = None

        # Use given elevation map or create random
        if initial_grid is not None:
            if rows != np.array(initial_grid).shape[0] or cols != np.array(initial_grid).shape[1]:
                raise ValueError('Shape of initial grid does not match given number of rows and columns.')

            self.grid = initial_grid
        else:
            self.grid = elevation_map(cols, rows, self.map_type)


