import time
import math
import re
import tkinter as tk
from collections import defaultdict


class Data:

    def __init__(self, name):
        file = open(name, "r")
        self.connections = Graph()
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
        file.close()

    @staticmethod
    def calc_distance(tuple1, tuple2):
        return math.sqrt(math.pow((tuple2[0] - tuple1[0]), 2) + math.pow((tuple2[1] - tuple1[1]), 2))

    def open_window(self):
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

    def draw_path(self, path):
        self.open_window()
        g = self.connections.get_graph()
        for vertex1 in g.keys():
            for vertex2, w in g[vertex1]:
                self.draw_edge(vertex1, vertex2, "black")

        for i in range(len(path) - 1):
            i += 1
            self.draw_edge(path[i - 1], path[i], "green")

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

    def get_graph(self):
        return self.graph


class Solve:

    def __init__(self, connections):
        self.connections = connections

    @staticmethod
    def get_gradient(a, b):
        if b[0] == a[0]:
            if b[1] > a[1]:
                return 100
            else:
                return -100
        val = (b[1] - a[1]) / (b[0] - a[0])
        if val == -0.0 or val == 0.0:
            return 0
        return (b[1] - a[1]) / (b[0] - a[0])

    def dijkstra(self, g, start, target):
        queue = [start]
        visited = set()
        distances = {start: 0}
        parents = {start: None}
        while queue:
            vertex1 = queue.pop(0)
            if vertex1 not in visited:
                visited.add(vertex1)
                for vertex2, w in g[vertex1]:
                    if vertex2 in visited:
                        continue
                    if distances.get(vertex2, None) is None or distances.get(vertex1) + w < distances.get(vertex2):
                        distances[vertex2] = distances.get(vertex1) + w
                        parents[vertex2] = vertex1
                        queue.append(vertex2)
        path = []
        cur = target
        while cur is not None:
            path.append(cur)
            cur = parents[cur]
        return distances, path

    def find_path(self, start, target, max_percentage):
        g = self.connections.get_graph()
        distances, shortest_path = self.dijkstra(g, target, start)
        max_dist = distances[start] * (1 + max_percentage / 100)

        queue = [start]
        visited = set()

        parents = {start: [Node(start, None, 200, 0, 0)]}
        while queue:
            vertex1 = queue.pop(0)
            for vertex2, weight in g[vertex1]:
                visited.add(vertex1)
                gradient = self.get_gradient(vertex1, vertex2)
                if vertex2 in visited:
                    continue
                if distances[vertex2] + parents[vertex1][0].get_distance() + weight > max_dist:
                    continue
                elif vertex1 == start:
                    parents[vertex2] = [Node(vertex2, parents[start], gradient, 0, weight)]
                    queue.append(vertex2)
                else:
                    turns = (parents[vertex1][0].get_turns()) + 1
                    total_distance = float("Inf")
                    for e in parents[vertex1]:
                        if e.get_gradient() == gradient:
                            turns -= 1
                            total_distance = e.get_distance() + weight
                            best_node = e
                            break
                        elif total_distance > e.get_distance() + weight:
                            total_distance = e.get_distance() + weight
                            best_node = e
                    if vertex2 not in parents.keys():
                        parents[vertex2] = [Node(vertex2, best_node, gradient, turns, total_distance)]
                        queue.append(vertex2)
                    else:
                        if turns == parents[vertex2][0].get_turns():
                            parents[vertex2].append(Node(vertex2, best_node, gradient, turns, total_distance))
                        elif turns < parents[vertex2][0].get_turns():
                            parents[vertex2] = [Node(vertex2, best_node, gradient, turns, total_distance)]
        # Output
        print("Abbiegungen:")
        print(parents[target][0].get_turns())
        print("Distanz:")
        print(str(parents[target][0].get_distance()) + " (" + str(
            100 * parents[target][0].get_distance() / distances[start] - 100) + "% longer than the shortest path)")
        # create path
        cur = parents[target][0].get_parent()
        path = [target]
        while type(cur) != list:  # get the path
            path.append(cur.get_node())
            cur = cur.get_parent()
        print("Pfad:")
        print(path)
        path.append(start)
        return path


class Node:

    def __init__(self, node, parent, gradient, turns, distance):
        self.node = node
        self.parent = parent
        self.gradient = gradient
        self.turns = turns
        self.distance = distance  # Distance from start

    def get_parent(self):
        return self.parent

    def get_gradient(self):
        return self.gradient

    def get_turns(self):
        return self.turns

    def get_distance(self):
        return self.distance

    def get_node(self):
        return self.node


print('Geben Sie die Nummer eines Beispiels ein:')
example = input()
print('Geben sie die maximale Verlängerung in Prozent an: ')
percent = int(input())

time1 = time.time()

d = Data("Beispiel" + example + ".txt")
s = Solve(d.connections)
result = s.find_path(d.start, d.target, percent)

print('In ' + str((time.time() - time1) / 1000) + ' Milliseconds')

# graphical output
d.draw_path(result)
d.finish()
