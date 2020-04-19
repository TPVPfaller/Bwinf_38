import time
import math
import re
import tkinter as tk
from collections import defaultdict
from itertools import permutations


class Data:

    def __init__(self, name):
        file = open(name, "r")
        self.graph = defaultdict(list)
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
                self.graph[pos1].append((pos2, self.calc_distance(pos1, pos2)))
                self.graph[pos2].append((pos1, self.calc_distance(pos1, pos2)))
                switch = True
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
        self.canvas.create_line(50 + tuple1[0] * 70 + 5, 550 - tuple1[1] * 70 + 5, 50 + tuple2[0] * 70 + 5,
                                550 - tuple2[1] * 70 + 5, fill=color, width=5)
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
        for vertex1 in self.graph.keys():
            for vertex2, w in self.graph[vertex1]:
                self.draw_edge(vertex1, vertex2, "black")

        for i in range(len(path) - 1):
            i += 1
            self.draw_edge(path[i - 1], path[i], "green")

    def finish(self):
        self.canvas.pack()
        tk.mainloop()


def find_best_path(graph, start, targets, max_percentage):
    distances = defaultdict()
    nodes = targets.copy()
    nodes.append(start)
    target_graph = defaultdict(list)
    for target1 in nodes:
        distances[target1] = (dijkstra(graph, start=target1))
        for target2 in nodes:
            if target1 != target2:
                target_graph[target1].append((target2, distances[target1][target2]))

    shortest = float("Inf")
    all_combs = []
    nodes.remove(start)
    for comb in permutations(nodes):
        total_distance = 0

        for i in range(len(comb)):
            if i == 0:
                for e, w in target_graph[start]:
                    if e == comb[0]:
                        total_distance += w
            else:
                for e, w in target_graph[comb[i-1]]:
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

    min_turns = float("Inf")
    best_dist = float("Inf")
    for targets, distance in paths:
        s = start
        limit = max_dist - distance
        total_turns = 0
        total_path = []
        total_distance = 0
        last_gradient = None
        for index, t in enumerate(targets):
            weight = 0
            for e, w in target_graph[s]:
                if e == t:
                    local_limit = limit + w
                    weight = w
            path, d, turns, l_gradient, f_gradient = turn_optimization(graph, s, t, local_limit, distances[t])
            if path == None:
                break
            total_turns += turns
            total_distance += d
            limit -= (d-weight)
            if 0 < index < len(targets) - 1:
                path.remove(t)
            for v in path:
                total_path.append(v)
            if last_gradient is not None:
                if abs(last_gradient) != abs(f_gradient):
                    total_turns += 1
            s = t
            last_gradient = l_gradient
        if total_turns < min_turns:
            best_path = total_path
            min_turns = total_turns
            best_dist = total_distance
        if total_turns == min_turns and total_distance < best_dist:
            best_path = total_path
            min_turns = total_turns
            best_dist = total_distance

    print("Maximale Distanz: " + str(max_dist))
    print("Pfad: ")
    print(best_path)
    print("Abbiegungen:", end=" ")
    print(min_turns)
    print("Distanz:")
    print(str(best_dist) + " (" + str(round(
        100 * best_dist / shortest - 100,
        4)) + "% länger als der kürzeste Pfad)")
    return best_path


def turn_optimization(graph, start, target, limit, distances):
    queue, visited = [start], set()
    nodes = {start: [Node(node=start, parent=None, gradient=0, turns=0, distance=0)]}
    while queue:  # dijkstra combined with finding least turns
        min_turns = []
        min_turn = float("Inf")
        for v in queue:  # Selecting the next node of the queue
            if nodes[v][0].turns <= min_turn:
                min_turn = nodes[v][0].turns
                min_turns.append(v)
        max_distance = -1
        for v in min_turns:
            if distances[v] > max_distance:    # If there are multiple vertices with same amount of turns select
                max_distance = distances[v]    # vertex with longest distance to target
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
            turns = nodes[vertex1][0].turns + 1
            total_distance = limit
            for e in nodes[vertex1]:    # Iterating through predecessors of vertex1
                if e.gradient == gradient:
                    turns -= 1
                    total_distance = e.distance + weight
                    best_node = e
                    break
                elif total_distance >= e.distance + weight:   # if there is no predecessor with same gradient
                    total_distance = e.distance + weight     # the vertex with the shortest distance gets selected
                    best_node = e
            if total_distance + distances[vertex2] > limit:
                continue
            if vertex2 not in nodes.keys() or turns < nodes[vertex2][0].turns:
                nodes[vertex2] = [Node(vertex2, best_node, gradient, turns, total_distance)]
                if vertex2 != target:
                    queue.append(vertex2)
            elif turns == nodes[vertex2][0].turns:
                nodes[vertex2].append(Node(vertex2, best_node, gradient, turns, total_distance))


    # Get shortest path
    shortest_distance = float("Inf")
    for e in nodes[target]:  # Iterate through all paths that go to target and have same amount of turns
        if e.distance < shortest_distance:
            shortest_distance = e.distance
            best = e
    # create path
    cur = best.parent
    path = [target]
    while type(cur) != list:
        path.append(cur.node)
        cur = cur.parent
    path.append(start)
    path = list(reversed(path))
    return path, shortest_distance, best.turns, get_gradient(path[-2], path[-1]), get_gradient(path[0], path[1])


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


print('Geben Sie die Nummer eines Beispiels ein:')
example = input()
print('Geben Sie die maximale Verlängerung in Prozent an: ')
percent = int(input())

time1 = time.time()
d = Data("Beispiel" + example + ".txt")
result = find_best_path(d.graph, d.start, d.targets, percent)

print('In ' + str((time.time() - time1) * 1000) + ' Milliseconds (with file reading, without graphics)')

# graphical output
d.draw_path(result)
d.finish()
