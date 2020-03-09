import math
import re
import itertools
import numpy
import tkinter as tk
from collections import defaultdict


class Data:

    def __init__(self, name):
        file = open(name, "r")
        self.connections = Graph()
        self.view_points()
        for line, val in enumerate(file.read().split()):
            if line == 1:
                x = re.search("(?P<teil1>[0-9]*),(?P<teil2>[0-9]*)", val)
                self.start = (int(x.group("teil1")), int(x.group("teil2")))
            elif line == 2:
                x = re.search("(?P<teil1>[0-9]*),(?P<teil2>[0-9]*)", val)
                self.target = (int(x.group("teil1")), int(x.group("teil2")))
            elif line > 2 and line % 2:
                x = re.search("(?P<teil1>[0-9]*),(?P<teil2>[0-9]*)", val)
                pos1 = (int(x.group("teil1")), int(x.group("teil2")))
            elif line > 2:
                x = re.search("(?P<teil1>[0-9]*),(?P<teil2>[0-9]*)", val)
                pos2 = (int(x.group("teil1")), int(x.group("teil2")))
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
        self.canvas.create_line(100 + tuple1[0] * 70 + 5, 900 - tuple1[1] * 70 + 5, 100 + tuple2[0] * 70 + 5, 900 - tuple2[1] * 70 + 5, fill = color, width = 5)
        self.canvas.create_oval(100 + tuple1[0] * 70, 900 - tuple1[1] * 70, 100 + tuple1[0] * 70 + 10, 900 - tuple1[1] * 70 + 10, fill = "red")
        self.canvas.create_oval(100 + tuple2[0] * 70, 900 - tuple2[1] * 70, 100 + tuple2[0] * 70 + 10, 900 - tuple2[1] * 70 + 10, fill = "red")
        if tuple1 == self.start or tuple1 == self.target:
            self.canvas.create_oval(100 + tuple1[0] * 70, 900 - tuple1[1] * 70, 100 + tuple1[0] * 70 + 10, 900 - tuple1[1] * 70 + 10, fill = "blue")
            if tuple2 == self.start or tuple2 == self.target:
                self.canvas.create_oval(100 + tuple2[0] * 70, 900 - tuple2[1] * 70, 100 + tuple2[0] * 70 + 10, 900 - tuple2[1] * 70 + 10, fill = "blue")

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

    def sort(self, queue):
        if not queue:
            return
        u = queue.pop(0)
        for v, w in self.graph[u]:
            if v not in self.nodes:
                self.nodes.append(v)
                queue.append(v)
        self.sort(queue)

    def get_nodes(self, data):
        q = [data.start]
        self.nodes.clear()
        self.nodes.append(data.start)
        self.sort(q)
        return self.nodes

    def get_nodes_reversed(self, data):
        q = [data.target]
        self.nodes.append(data.target)
        self.sort(q)
        return self.nodes

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
    def get_if_straight(a, b, c):
        vector_a = numpy.subtract(b, a)
        vector_b = numpy.subtract(b, c)
        return round(math.degrees(numpy.arccos(numpy.dot(vector_a, vector_b) / (
                    math.sqrt((vector_a[0] ** 2) + (vector_a[1] ** 2)) * math.sqrt((vector_b[0] ** 2) +
                                                                                (vector_b[1] ** 2)))))) != 180

    def find_path(self, start, target, max_percentage):
        print(start, target)
        nodes = self.connections.get_nodes_reversed(self.data)  # From target to start
        g = self.connections.get_graph()
        dist_to_target = defaultdict()
        parent = defaultdict()
        for e in nodes:
            dist_to_target[e] = float("Inf")
            parent[e] = None
        dist_to_target[target] = 0

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
        nodes = self.connections.get_nodes(self.data)   # From start to target
        max_dist = dist_to_target[start] * (1+max_percentage/100)
        best = defaultdict()
        self.get_if_straight((0, 0), (0, 1), (0, 2))
        for e in nodes:
            best[e] = [float("Inf"), float("Inf")]  # [0] := turns, [1] := distance
            parent[e] = None
        best[start][0] = 0
        best[start][1] = 0
        for e, dist in g[start]:
            best[e] = [0, dist]
        for s in nodes:
            for middle, weightM in g[s]:
                if middle == target or s == target:
                    break
                if dist_to_target[s] + weightM < dist_to_target[middle]:
                    dist_to_target[middle] = dist_to_target[s] + middle
                for tar, weightT in g[middle]:
                    if s != middle and middle != tar and s != tar:
                        #print(best[s][0])
                        print(s, middle, tar)
                        print(int(self.get_if_straight(s, middle, tar)))
                        if (best[s][1] + weightM + weightT + dist_to_target[tar]) <= max_dist:
                            if best[s][0] + int(self.get_if_straight(s, middle, tar)) < best[tar][0]:
                                best[tar][0] = best[s][0] + int(self.get_if_straight(s, middle, tar))
                                parent[tar] = middle
                                parent[middle] = s
                                best[tar][1] = best[s][1] + weightT + weightM

        print(best[target])
        x = target
        path = []
        print(best)
        while x:
            path.append(x)
            x = parent[x]
        print(path)

        self.data.draw_path(path)
        self.data.finish()


d = Data("Beispiel1.txt")
d.connections.print()

s = Solve(d)
s.find_path(d.start, d.target, 15)
