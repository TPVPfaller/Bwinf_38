import collections

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
                self.draw_edge(pos1, pos2, "black")
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

    def print(self):
        for u in self.graph:
            print(str(u) + ":", end=" [")
            counter = 1
            for v, w in self.graph[u]:
                if len(self.graph[u]) != counter:
                    print("(" + str(v) + " - distance: " + str(w), end="),  ")
                else:
                    print("(" + str(v) + " - distance: " + str(w), end=")], ")
                counter += 1
        print('-')

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
        print(start, target)
        nodes = self.connections.get_nodes(target)  # From target to start
        g = self.connections.get_graph()
        dist_to_target = defaultdict()
        parent = defaultdict()
        for e in nodes:
            dist_to_target[e] = float("Inf")
            parent[e] = None
        dist_to_target[target] = 0
        print(nodes)
        for current in nodes:
            for node, weight in g[current]:
                if dist_to_target[current] + weight < dist_to_target[node]:
                    dist_to_target[node] = dist_to_target[current] + weight
                    parent[node] = current
        for e in nodes:
            print(dist_to_target[e])  # print distance from target to the all nodes
        x = start
        path = []

        while x:
            path.append(x)
            x = parent[x]
        nodes = self.connections.get_nodes(start)  # From start to target
        max_dist = dist_to_target[start] * (1 + max_percentage / 100)
        best = defaultdict()
        self.get_gradient((0, 0), (0, 1))
        for e in nodes:
            parent[e] = None
        print(nodes)
        test = defaultdict()
        parent[start] = [Parent(start, 200, 0)]
        for s in nodes:
            for tar, weight in g[s]:
                gradient = self.get_gradient(s, tar)
                if tar == start:
                    pass
                elif s == start:
                    parent[tar] = [Parent(s, gradient, 0)]
                else:
                    turns = (parent[s][0].getTurns())
                    turns += 1
                    for e in parent[s]:
                        if e.getGradient() == gradient:
                            turns -= 1
                            test[tar] = i
                            break
                    if parent[tar] is None:
                        parent[tar] = [Parent(s, gradient, turns)]
                    else:
                        if turns < parent[tar][0].getTurns():
                            parent[tar] = [Parent(s, gradient, turns)]
                        elif turns == parent[tar][0].getTurns():
                            parent[tar].append(Parent(s, gradient, turns))
        print(parent)
        cur = target
        print(parent[cur][0].getTurns())
        result = []
        print(test)
        while parent[cur][0].getGradient() != 200:
            if len(parent[cur]) > 1:
                cur = parent[cur][test[cur]].getNode()
            else:
                cur = parent[cur][0].getNode()
            result.append(cur)
            print(cur)
        print(result)
        self.data.draw_path(result)
        self.data.finish()


class Parent:
    node = (0, 0)
    gradient = 0
    turns = 0

    def __init__(self, node, gradient, turns):
        self.node = node
        self.gradient = gradient
        self.turns = turns

    def getNode(self):
        return self.node

    def getGradient(self):
        return self.gradient

    def getTurns(self):
        return self.turns


d = Data("Beispiel1.txt")
d.connections.print()

s = Solve(d)
s.find_path(d.start, d.target, 15)
