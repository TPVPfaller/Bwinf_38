import collections
from collections import defaultdict
import numpy as np


class Graph:

    def __init__(self):
        self.graph = defaultdict(list)
        self.nodes = []

    def add_edge(self, u_tuple, v_tuple, w):
        self.graph[u_tuple].append((v_tuple, w))
        self.graph[v_tuple].append((u_tuple, w))

    def get_nodes(self, root):
        visited = []
        queue = collections.deque([root])
        visited.append(root)
        while queue:
            vertex = queue.popleft()
            for neighbour, w in self.graph[vertex]:
                if neighbour not in visited:
                    visited.append(neighbour)
                    queue.append(neighbour)
        return visited

    def get_graph(self):
        return self.graph


filename = "Beispiel0.txt"


#   Read Data
file = open(filename, "r")
batteries = []
for line, val in enumerate(file.read().split()):
    if line == 0:
        grid = np.zeros((int(val), int(val)))
    elif line == 1:
        robot = tuple(val.split(","))
    elif line == 2:
        pass
    else:
        battery = tuple(val.split(","))
        batteries.append(battery)
        grid[int(battery[1]) - 1][int(battery[0]) - 1] = int(battery[2])
file.close()

graph = Graph()

print(batteries)
batteries.sort()
print(batteries)
print(grid)
