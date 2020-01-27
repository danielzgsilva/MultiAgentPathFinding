import os 
import argparse
from utils import coords

file_dir = os.path.dirname(__file__)

class PathFindingOptions:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Multi-agent pathfinding options')

        self.required = self.parser.add_argument_group('required arguments')
        self.optional = self.parser.add_argument_group('optional arguments')

        self.required.add_argument('--num_agents',
                                 type = int,
                                 help = 'number of agents to spawn into the world',
                                 required = True)

        self.required.add_argument('--starts',
                                 type = coords,
                                 help = 'list of x, y start coordinates for each agent',
                                 nargs = '+',
                                 required = True)

        self.required.add_argument('--goals',
                                 type = coords,
                                 help = 'list of x, y goal coordinates for each agent',
                                 nargs = '+',
                                 required = True)

        self.required.add_argument('--max_time',
                                   type = int,
                                   help = 'maximum amount of time each agent has to each its goal',
                                   required = True)

        self.optional.add_argument("--width",
                                 type = int,
                                 help = 'width of the grid',
                                 default = 20)

        self.optional.add_argument("--height",
                                 type = int,
                                 help = 'height of the grid',
                                 default = 20)

        self.optional.add_argument('--map_type',
                                 type = str,
                                 help = 'type of map to create',
                                 default = 'combined',
                                 choices = ['mountains', 'plains', 'canyons', 'combined'])

        self.optional.add_argument('--no_viz',
                                   help = 'if set, will not run the path finding visualization',
                                   action = 'store_true')

    def parse(self):
        self.options = self.parser.parse_args()
        return self.options