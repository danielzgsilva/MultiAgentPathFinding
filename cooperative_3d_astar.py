from elevation_astar import AStarPathFinder
from reservation_table import ReservationTable
from timeit import default_timer as timer
from simulation import OpenGl_Viz


class CooperativePathFinder:
    def __init__(self, map, agents, max_time, no_viz):
        self.map = map
        self.agents = agents
        self.max_time = max_time
        self.viz = None

        if not no_viz:
            self.viz = OpenGl_Viz(map, max_time)

    def find_paths(self):
        start = timer()

        # Create time-space reservation table
        reservations = ReservationTable(self.map.cols, self.map.rows, self.max_time)

        paths = dict()

        # Initialize agent start locations
        for agent in self.agents:
            paths[agent.num] = []
            for t in range(self.max_time):
                reservations.set_blocked(agent.sx, agent.sy, t)

        # Initialize and display elevation map and agents
        if self.viz:
            self.viz.initialize(self.agents)

        print('Planning paths for {} agents'.format(len(self.agents)))
        for agent in self.agents:
            print('--> Agent {} starting at {} going to {}'.format(agent.num, (agent.sx, agent.sy), (agent.fx, agent.fy)))
            path_finder = AStarPathFinder(reservations, self.map)

            # Run single agent a* for each agent
            path = path_finder.find_path(agent, self.viz)

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

        # Simulate agent's moving along their paths
        if self.viz:
            self.viz.simulate(paths)

        return paths
