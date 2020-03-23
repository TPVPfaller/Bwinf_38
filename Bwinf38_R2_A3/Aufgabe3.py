import collections
import time
import math
import re
import tkinter as tk
from collections import defaultdict


class Data:

    def __init__(self, name):
        file = open(name, "r")
        self.connections = Graph()
        self.view_points()
        for line, val in enumerate(file.read().split()):
            if line == 1:
                x = re.search("(?P<part1>[0-9]*),(?P<part2>[0-9]*)", val)
                self.start = (int(x.group("part1")), int(x.group("part2")))
            elif line == 2:
                x = re.search("(?P<part1>[0-9]*),(?P<part2>[0-9]*)", val)
                self.target = (int(x.group("part1")), int(x.group("part2")))
            elif line > 2 and line % 2:
                x = re.search("(?P<part1>[0-9]*),(?P<part2>[0-9]*)", val)
                pos1 = (int(x.group("part1")), int(x.group("part2")))
            elif line > 2:
                x = re.search("(?P<part1>[0-9]*),(?P<part2>[0-9]*)", val)
                pos2 = (int(x.group("part1")), int(x.group("part2")))
                self.connections.add_edge(pos1, pos2, self.calc_distance(pos1, pos2))
                #self.draw_edge(pos1, pos2, "black")
        file.close()

    @staticmethod
    def calc_distance(tuple1, tuple2):
        return math.sqrt(math.pow((tuple2[0] - tuple1[0]), 2) + math.pow((tuple2[1] - tuple1[1]), 2))

    def view_points(self):
        root = tk.Tk()
        root.title("IDINA")
        root.geometry("1200x1000+300+20")
        self.canvas = tk.Canvas(root, bg="white", height=1000, width=1200)

    def draw_edge(self, tuple2, tuple1, color):
        self.canvas.create_line(100 + tuple1[0] * 70 + 5, 900 - tuple1[1] * 70 + 5, 100 + tuple2[0] * 70 + 5,
                                900 - tuple2[1] * 70 + 5, fill=color, width=5)
        self.canvas.create_oval(100 + tuple1[0] * 70, 900 - tuple1[1] * 70, 100 + tuple1[0] * 70 + 10,
                                900 - tuple1[1] * 70 + 10, fill="red")
        self.canvas.create_oval(100 + tuple2[0] * 70, 900 - tuple2[1] * 70, 100 + tuple2[0] * 70 + 10,
                                900 - tuple2[1] * 70 + 10, fill="red")
        if tuple1 == self.start or tuple1 == self.target:
            self.canvas.create_oval(100 + tuple1[0] * 70, 900 - tuple1[1] * 70, 100 + tuple1[0] * 70 + 10,
                                    900 - tuple1[1] * 70 + 10, fill="blue")
            if tuple2 == self.start or tuple2 == self.target:
                self.canvas.create_oval(100 + tuple2[0] * 70, 900 - tuple2[1] * 70, 100 + tuple2[0] * 70 + 10,
                                        900 - tuple2[1] * 70 + 10, fill="blue")

    def draw_path(self, list):
        for i in range(len(list) - 1):
            i += 1
            self.draw_edge(list[i - 1], list[i], "green")

    def finish(self):
        self.canvas.pack()
        tk.mainloop()


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

    def get_distance(self, node1, node2):
        for e in self.graph[node1]:
            if e == node2:
                return e[1]
        return 'ERROR'

    def get_graph(self):
        return self.graph

    def get_length(self):
        return len(self.graph)


class Solve:

    def __init__(self, data):
        self.data = data
        self.connections = data.connections

    def calc_weights(self):
        for pos1 in self.connections:
            for pos2 in self.connections[pos1]:
                self.connections[pos1].append()

    @staticmethod
    def get_gradient(a, b):
        if b[0] == a[0]:
            if b[1] > a[1]:
                return 100
            else:
                return -100
        elif (b[1] - a[1]) / (b[0] - a[0]) == -0.0 or (b[1] - a[1]) / (b[0] - a[0]) == 0.0:
            return 0
        else:
            return (b[1] - a[1]) / (b[0] - a[0])

    def find_path(self, start, target, max_percentage):
        nodes = self.connections.get_nodes(target)  # From target to start
        g = self.connections.get_graph()
        dist_to_target = defaultdict()
        parents = defaultdict()
        for e in nodes:
            dist_to_target[e] = float("Inf")
            parents[e] = None
        dist_to_target[target] = 0
        for current in nodes: # Dijkstra
            for node, weight in g[current]:
                if dist_to_target[current] + weight < dist_to_target[node]:
                    dist_to_target[node] = dist_to_target[current] + weight
                    parents[node] = current
        nodes = self.connections.get_nodes(start)  # From start to target
        max_dist = dist_to_target[start] * (1 + max_percentage / 100)
        best = defaultdict()
        self.get_gradient((0, 0), (0, 1))
        for e in nodes:
            parents[e] = None
        parents[start] = [Node(start, None, 200, 0, 0)]
        for s in nodes:
            for tar, weight in g[s]:
                distance = Data.calc_distance(s, tar)
                gradient = self.get_gradient(s, tar)
                if parents[s] is None:
                    pass
                elif dist_to_target[tar] + parents[s][0].getDistance() + distance > max_dist:
                    pass
                elif tar == start:
                    pass
                elif s == start:
                    parents[tar] = [Node(tar, parents[start], gradient, 0, distance)]
                else:
                    turns = (parents[s][0].getTurns())
                    turns += 1
                    totalDistance = float("Inf")
                    for e in parents[s]:
                        if e.getGradient() == gradient:
                            turns -= 1
                            totalDistance = e.getDistance() + distance
                            bestNode = e
                            break
                        elif totalDistance > e.getDistance() + distance:
                            totalDistance = e.getDistance() + distance
                            bestNode = e
                    if parents[tar] is None:
                        parents[tar] = [Node(tar, bestNode, gradient, turns, totalDistance)]
                    else:
                        if turns < parents[tar][0].getTurns():
                            parents[tar] = [Node(tar, bestNode, gradient, turns, totalDistance)]
                        elif turns == parents[tar][0].getTurns():
                            parents[tar].append(Node(tar, bestNode, gradient, turns, totalDistance))
        print(parents[target][0].getTurns())
        cur = parents[target][0].getParent()
        result = []
        result.append(target)
        while type(cur) != list:
            result.append(cur.getNode())
            cur = cur.getParent()
        print(result)
        result.append(start)
        return result


class Node:

    def __init__(self, node, parent, gradient, turns, distance):
        self.node = node
        self.parent = parent
        self.gradient = gradient
        self.turns = turns
        self.distance = distance  # Distance from start

    def getParent(self):
        return self.parent

    def getGradient(self):
        return self.gradient

    def getTurns(self):
        return self.turns

    def getDistance(self):
        return self.distance

    def getNode(self):
        return self.node


d = Data("Beispiel2.txt")
time1 = time.time()
s = Solve(d)
result = s.find_path(d.start, d.target, 15)
time2 = time.time()

#d.draw_path(result)
#d.finish()
print('In ' + str(round((time2 - time1), 10) * 1000) + ' Milliseconds')