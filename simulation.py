import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import PyQt5 as Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, \
    QVBoxLayout, QWidget

import sys
import matplotlib as plt
import random as rand

class OpenGl_Viz(object):
    def __init__(self, map, max_time):
        """
        Initialize the graphics window and mesh
        """
        self.map = map
        self.paths = {}
        self.max_time = max_time
        self.t = 0
        self.agents = {}
        self.timer = QtCore.QTimer()

        # setup the view window
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.w.setGeometry(0, 0, 1920, 1080)
        self.w.show()
        self.w.setWindowTitle('Multi Agent Path Finding')
        self.w.setCameraPosition(distance = 50, elevation = 50, azimuth = 225)

        # Set up 3d surface plot
        x = np.arange(0, map.cols) - map.cols // 2
        y = np.arange(0, map.rows) - map.rows // 2
        cmap = plt.cm.get_cmap('jet')
        minZ = np.min(map.grid)
        maxZ = np.max(map.grid)
        rgba_img = cmap((map.grid - minZ) / (maxZ - minZ))

        # Create and display surface plot
        self.surface = gl.GLSurfacePlotItem(x = y, y = x, z = map.grid, colors = rgba_img)
        self.w.addItem(self.surface)

    def start(self):
        """
        get the graphics window open and setup
        """
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def initialize(self, agents):
        start_color = np.array([0.0, 1.0, 0.0, 1.0]).reshape((1, 4))
        end_color = np.array([1.0, 0.0, 0.0, 1.0]).reshape((1, 4))

        for agent in agents:
            start = np.array([agent.sy - self.map.rows // 2, agent.sx - self.map.cols // 2,
                              self.map.grid[agent.sy][agent.sx]]).reshape((1, 3))

            agent_symbol = gl.GLScatterPlotItem(pos = start, color = start_color, size = 20)
            self.agents[agent.num] = agent_symbol
            self.w.addItem(agent_symbol)

            end = np.array([agent.fy - self.map.rows // 2, agent.fx - self.map.cols // 2,
                            self.map.grid[agent.fy][agent.fx]]).reshape((1, 3))

            goal = gl.GLScatterPlotItem(pos = end, color = end_color, size = 20)
            self.w.addItem(goal)

        self.app.processEvents()

    def show_path(self, cur_agent = None, cur_path=None):

        self.erase_path(cur_path)
        cur_path = None

        points = []
        for node in self.paths[cur_agent]:
            point = [node[1] - self.map.rows // 2, node[0] - self.map.cols // 2,
                              self.map.grid[node[1]][node[0]]]
            points.append(point)

        points = np.array(points).reshape((-1, 3))
        path_line = gl.GLLinePlotItem(pos = points, width = 4, mode = 'line_strip', antialias=True)

        cur_path = path_line

        self.w.addItem(path_line)

        self.app.processEvents()
        return cur_path

    def move_agents(self):
        '''
        Move each agent to its next time step
        '''

        # Move agents
        for agent, agent_symbol in self.agents.items():
            path = self.paths[agent]
            if path and self.t < self.max_time:
                point = np.array([path[self.t][1] - self.map.rows // 2, path[self.t][0] - self.map.cols // 2,
                                  self.map.grid[path[self.t][1]][path[self.t][0]]]).reshape((1, 3))

                agent_symbol.setData(pos = point)
                self.t += 1

            elif self.t >= self.max_time:
                self.t = 0
                self.timer.stop()

    def erase_path(self, path):
        if path:
            self.w.removeItem(path)

    def simulate(self, paths):
        """
        calls the move_agents method to run in a loop
        """

        self.paths = paths
        self.timer.timeout.connect(self.move_agents)
        self.timer.start(500)
        self.start()
        self.move_agents()
