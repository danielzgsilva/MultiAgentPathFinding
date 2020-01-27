import os 
import argparse

file_dir = os.path.dirname(__file__)

class PathFindingOptions:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Multi-agent pathfinding options')

        self.parser.add_argument("--width",
                                 type = int,
                                 help = 'width of the grid',
                                 default = 20)

        self.parser.add_argument("--height",
                                 type = int,
                                 help = 'height of the grid',
                                 default = 20)

        self.parser.add_argument('--num_agents',
                                 type = int,
                                 help = 'number of agents to spawn into the world')

        self.parser.add_argument('--')

