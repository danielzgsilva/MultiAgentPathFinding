from options import PathFindingOptions
from map import ElevationMap
from cooperative_3d_astar import CooperativePathFinder
from agent import Agent

if __name__ == '__main__':
    options = PathFindingOptions()

    # Parse args
    opts = options.parse()

    # Create elevation map
    map = ElevationMap(opts.height, opts.width, opts.map_type, initial_grid=None)

    if opts.num_agents != len(opts.starts) or opts.num_agents != len(opts.goals):
        raise AssertionError('Number of agents does not match number of start or goal coordinates')

    # Create some agents
    agents = list()

    for i in range(opts.num_agents):
        # Start coordinates
        sx = opts.starts[i][0]
        sy = opts.starts[i][1]

        # Goal coordinates
        fx = opts.goals[i][0]
        fy = opts.goals[i][1]

        agents.append(Agent(i, sx, sy, fx, fy))

    # Plan and visualize paths for the agents
    agent_planner = CooperativePathFinder(map, agents, opts.max_time, opts.no_viz)
    paths = agent_planner.find_paths()




