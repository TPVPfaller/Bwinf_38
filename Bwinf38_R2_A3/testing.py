import time
import math
import re
import tkinter as tk
from collections import defaultdict
from itertools import permutations

class Data:

    def __init__(self, name):
        file = open(name, "r")
        self.connections = Graph()
        switch = True
        self.targets = []
        for line, val in enumerate(file.read().split()):
            if line == 0:
                continue
            elif line == 1:
                self.target_count = int(val)
            elif line == 2:
                x = re.search("(?P<part1>[0-9]*),(?P<part2>[0-9]*)", val)
                self.start = (int(x.group("part1")), int(x.group("part2")))
            elif line <= 2 + self.target_count:
                x = re.search("(?P<part1>[0-9]*),(?P<part2>[0-9]*)", val)
                self.targets.append((int(x.group("part1")), int(x.group("part2"))))
            elif line > 2 + self.target_count and switch:
                x = re.search("(?P<part1>[0-9]*),(?P<part2>[0-9]*)", val)
                pos1 = (int(x.group("part1")), int(x.group("part2")))
                switch = False
            elif line > 2 + self.target_count:
                x = re.search("(?P<part1>[0-9]*),(?P<part2>[0-9]*)", val)
                pos2 = (int(x.group("part1")), int(x.group("part2")))
                self.connections.add_edge(pos1, pos2, self.calc_distance(pos1, pos2))
                switch = True

        print(self.targets)
        file.close()

    @staticmethod
    def calc_distance(tuple1, tuple2):
        return math.sqrt(math.pow((tuple2[0] - tuple1[0]), 2) + math.pow((tuple2[1] - tuple1[1]), 2))

    def open_window(self):
        root = tk.Tk()
        root.title("Aufgabe3")
        root.geometry("1200x800+0+0")
        self.canvas = tk.Canvas(root, bg="white", height=800, width=1200)

    def draw_edge(self, tuple2, tuple1, color):

        self.canvas.create_line(50 + tuple1[0] * 70 + 5, 550 - tuple1[1] * 70 + 5, 50 + tuple2[0] * 70 + 5, 550 - tuple2[1] * 70 + 5, fill=color, width=5)
        self.canvas.create_oval(50 + tuple1[0] * 70, 550 - tuple1[1] * 70, 50 + tuple1[0] * 70 + 10,
                                550 - tuple1[1] * 70 + 10, fill="red")
        self.canvas.create_oval(50 + tuple2[0] * 70, 550 - tuple2[1] * 70, 50 + tuple2[0] * 70 + 10,
                                550 - tuple2[1] * 70 + 10, fill="red")
        if tuple1 == self.start or tuple1 in self.targets:
            self.canvas.create_oval(50 + tuple1[0] * 70, 550 - tuple1[1] * 70, 50 + tuple1[0] * 70 + 10,
                                    550 - tuple1[1] * 70 + 10, fill="blue")
        if tuple2 == self.start or tuple2 in self.targets:
            self.canvas.create_oval(50 + tuple2[0] * 70, 550 - tuple2[1] * 70, 50 + tuple2[0] * 70 + 10,
                                    550 - tuple2[1] * 70 + 10, fill="blue")

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

    def add_edge(self, u_tuple, v_tuple, w):
        self.graph[u_tuple].append((v_tuple, w))
        self.graph[v_tuple].append((u_tuple, w))

    def add_single_edge(self, u_tuple, v_tuple, w):
        self.graph[u_tuple].append((v_tuple, w))

    def get_graph(self):
        return self.graph


def find_best_path(graph, start, targets, max_percentage):
    distances = []
    nodes = targets.copy()
    nodes.append(start)
    target_graph = Graph()
    for target1 in nodes:
        distances.append(dijkstra(graph, start=target1))
        for target2 in nodes:
            if target1 != target2:
                target_graph.add_single_edge(target1, target2, distances[-1][target2])
    g = target_graph.get_graph()
    shortest = float("Inf")
    all_combs = []
    nodes.remove(start)
    for comb in permutations(nodes):
        total_distance = 0

        for i in range(len(comb)):
            if i == 0:
                for e, w in g[start]:
                    if e == comb[0]:
                        total_distance += w
            else:
                for e, w in g[comb[i-1]]:
                    if e == comb[i]:
                        total_distance += w
        if total_distance < shortest:
            shortest = total_distance

        all_combs.append((list(comb), total_distance))
    max_dist = shortest * (1 + max_percentage / 100)
    paths = []
    for c, d in all_combs:
        if d <= max_dist:
            paths.append((c, d))
            
    print(paths)
    print("Maximale Distanz: " + str(max_dist))
    print(shortest)
    print(target_graph.get_graph())
    print(distances)
    # # Output
    # print("Abbiegungen:")
    # print(parents[target][0].get_turns())
    # print("Distanz:")
    # print(str(parents[target][0].get_distance()) + " (" + str(round(
    #     100 * parents[target][0].get_distance() / distances[start] - 100,
    #     4)) + "% longer than the shortest path)")
    # # create path
    # cur = parents[target][0].get_parent()
    # path = [target]
    # while type(cur) != list:
    #     path.append(cur.get_node())
    #     cur = cur.get_parent()
    # path.append(start)
    # print("Pfad:")
    # print(path)
    # return path


def get_gradient(a, b):
    if b[0] == a[0]:  # vertical
        if b[1] > a[1]:
            return float("Inf")
        else:
            return -float("Inf")
    val = (b[1] - a[1]) / (b[0] - a[0])
    return val


def dijkstra(graph, start):
    queue = [start]
    visited = set()
    distances = {start: 0}
    parents = {start: None}
    while queue:
        minimum = float("Inf")
        for v in queue:
            if distances[v] < minimum:
                minimum = distances[v]
                vertex1 = v
        queue.remove(vertex1)
        if vertex1 not in visited:
            visited.add(vertex1)
            for vertex2, weight in graph[vertex1]:  # weight := distance between the two vertices
                if vertex2 in visited:
                    continue
                # Updating distance if distance isn't set yet or the distance is shorter than the previous distance
                if distances.get(vertex2, None) is None or distances.get(vertex1) + weight < distances.get(vertex2):
                    distances[vertex2] = distances.get(vertex1) + weight
                    parents[vertex2] = vertex1
                    queue.append(vertex2)
    return distances
# Erweiterung: Mehrere Ziele, die alle erreicht werden müssen


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
print('Geben Sie die maximale Verlängerung in Prozent an: ')
percent = int(input())

time1 = time.time()
d = Data("Beispiel" + example + ".txt")
result = find_best_path(d.connections.get_graph(), d.start, d.targets, percent)

print('In ' + str((time.time() - time1) * 1000) + ' Milliseconds (with file reading, without graphics)')

# graphical output
d.draw_path([(0, 0), (0, 1)])
d.finish()
