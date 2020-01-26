from elevation_astar import AStarPathFinder
from map import ElevationMap
from reservation_table import ReservationTable
from agent import Agent
import os
from timeit import default_timer as timer
from simulation import OpenGl_Viz

class CooperativePathFinder:
    def __init__(self, map, agents, max_time):
        self.map = map
        self.agents = agents
        self.max_time = max_time
        self.viz = OpenGl_Viz(map)
        self.viz.max_time = max_time

    def find_paths(self):

        start = timer()

        # Create time-space reservation table
        reservations = ReservationTable(self.map.cols, self.map.rows, self.max_time)
        #print(np.array(reservations.table))

        #print('Created reservation table in {}'.format(timer() - start))
        paths = {}

        # Initialize agent start locations
        for agent in self.agents:
            paths[agent.num] = []
            for t in range(reservations.time):
                reservations.set_blocked(agent.sx, agent.sy, t)

        self.viz.initialize(self.agents)

        print('Planning paths for {} agents'.format(len(agents)))
        for agent in self.agents:
            print('Agent {} starting at {} going to {}'.format(agent.num, (agent.sx, agent.sy), (agent.fx, agent.fy)))
            path_finder = AStarPathFinder(reservations, self.map)

            # Run single agent a* for each agent
            path = path_finder.find_path(agent.sx, agent.sy, agent.fx, agent.fy)

            # Save the path for each agent
            paths[agent.num] = path

            # Record this agent's movement in the reservation table
            for x, y, t in path[1:]:
                reservations.set_blocked(x, y, t)
                reservations.set_blocked(x, y, t + 1)
                reservations.set_blocked(x, y, t - 1)
                reservations.unblock(agent.sx, agent.sy, t)

            # Fill the remaining time slots in the reservation table with the agent's final location
            fx, fy, ft = path[-1]
            ft += 1
            while ft < self.max_time:
                reservations.set_blocked(fx, fy, ft)
                reservations.unblock(agent.sx, agent.sy, ft)
                ft += 1

        self.viz.animate(paths)
        return paths

if __name__ == "__main__":
    rows = 20
    cols = 20
    # Create random elevation map
    map = ElevationMap(w=400, h=400, rows=rows, cols=cols, initial_grid=None)

    # Create some agents
    agents = list()
    agents.append(Agent(0, 0, 0, cols-1, rows-1))
    agents.append(Agent(1, 0, rows-1, cols-1, 0))
    '''agents.append(Agent(2, cols-1, 1, 1, rows - 1))
    agents.append(Agent(3, cols-2, rows-1, 0, 1))'''

    # Arbitrary max time limit
    max_time = (rows + cols)

    # Plan paths for the agents
    agent_planner = CooperativePathFinder(map, agents, max_time)
    paths = agent_planner.find_paths()

    # Display map and paths
    #vid_path = os.path.join(os.getcwd(), 'simulations')
    #map.animate(agents, paths, vid_path, agent_planner.max_time)
    #map.show_grid(agents, paths)