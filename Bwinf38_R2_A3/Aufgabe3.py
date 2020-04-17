import time
import math
import re
import tkinter as tk
from collections import defaultdict


class Data:

    def __init__(self, name):
        file = open(name, "r")
        self.graph = defaultdict(list)
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
                self.graph[pos1].append((pos2, self.calc_distance(pos1, pos2)))
                self.graph[pos2].append((pos1, self.calc_distance(pos1, pos2)))
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
        if tuple1 == self.start or tuple1 == self.target:
            self.canvas.create_oval(50 + tuple1[0] * 70, 550 - tuple1[1] * 70, 50 + tuple1[0] * 70 + 10,
                                    550 - tuple1[1] * 70 + 10, fill="blue")
        if tuple2 == self.start or tuple2 == self.target:
            self.canvas.create_oval(50 + tuple2[0] * 70, 550 - tuple2[1] * 70, 50 + tuple2[0] * 70 + 10,
                                    550 - tuple2[1] * 70 + 10, fill="blue")

    def draw_path(self, path):
        self.open_window()
        for vertex1 in self.graph.keys():
            for vertex2, w in self.graph[vertex1]:
                self.draw_edge(vertex1, vertex2, "black")

        for i in range(len(path) - 1):
            i += 1
            self.draw_edge(path[i - 1], path[i], "green")

    def finish(self):
        self.canvas.pack()
        tk.mainloop()


def find_best_path(graph, start, target, max_percentage):
    distances = dijkstra(graph, start=target)  # distances relative to target
    limit = distances[start] * (1 + max_percentage / 100)
    queue = [start]
    nodes = {start: [Node(node=start, parent=None, gradient=200, turns=0, distance=0)]}
    # dijkstra combined with finding least turns
    visited = set()
    while queue:
        min_turns = []
        min_turn = float("Inf")
        #   Selecting the next node of the queue
        for v in queue:
            if nodes[v][0].get_turns() <= min_turn:
                min_turn = nodes[v][0].get_turns()
                min_turns.append(v)
        max_distance = -1
        for v in min_turns:
            if distances[v] > max_distance:    # If there are multiple vertices with the same amount of turns select
                max_distance = distances[v]    # the one with the longest Distance to the target
                vertex1 = v
        queue.remove(vertex1)
        visited.add(vertex1)
        for vertex2, weight in graph[vertex1]:
            if vertex2 in visited:
                continue
            gradient = get_gradient(vertex1, vertex2)
            if vertex1 == start:
                nodes[vertex2] = [Node(vertex2, nodes[start], gradient, 0, weight)]
                queue.append(vertex2)
                continue
            turns = (nodes[vertex1][0].get_turns()) + 1
            total_distance = float("Inf")
            for e in nodes[vertex1]:    # Iterating through predecessors of vertex1
                if e.get_gradient() == gradient and e.get_distance() + weight + distances[vertex2] <= limit:
                    turns -= 1
                    total_distance = e.get_distance() + weight
                    best_node = e
                    break
                elif total_distance > e.get_distance() + weight:   # if there is no predecessor with the same gradient
                    total_distance = e.get_distance() + weight     # the vertex with the shortest distance gets selected
                    best_node = e
            if best_node.get_distance() + weight + distances[vertex2] > limit:
                continue
            if vertex2 not in nodes.keys():
                nodes[vertex2] = [Node(vertex2, best_node, gradient, turns, total_distance)]
                if vertex2 != target and vertex2 not in queue:
                    queue.append(vertex2)
            else:
                if turns == nodes[vertex2][0].get_turns():
                    nodes[vertex2].append(Node(vertex2, best_node, gradient, turns, total_distance))
                elif turns < nodes[vertex2][0].get_turns():
                    nodes[vertex2] = [(Node(vertex2, best_node, gradient, turns, total_distance))]
                    if vertex2 != target and vertex2 not in queue:
                        queue.append(vertex2)
    # Get path with least distance
    least_distance = float("Inf")
    for e in nodes[target]:  # Iterate through all paths that go to path and have the same amount of turns
        if e.get_distance() < least_distance:
            least_distance = e.get_distance()
            best = e
    print("Abbiegungen:")
    print(best.get_turns())
    print("Distanz:")
    print(str(best.get_distance()) + " (" + str(round(
        100 * best.get_distance() / distances[start] - 100,
        4)) + "% longer than the shortest path)")
    # create path
    cur = best.get_parent()
    path = [target]
    while type(cur) != list:
        path.append(cur.get_node())
        cur = cur.get_parent()
    path.append(start)
    print("Pfad:")
    print(path)
    return path


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
    while queue:
        minimum = float("Inf")
        for v in queue:  # linear search
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
                if distances.get(vertex2) is None or distances.get(vertex1) + weight < distances.get(vertex2):
                    distances[vertex2] = distances.get(vertex1) + weight
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
result = find_best_path(d.graph, d.start, d.target, percent)

print('In ' + str((time.time() - time1) * 1000) + ' Milliseconds (with file reading, without graphics)')

# graphical output
d.draw_path(result)
d.finish()
