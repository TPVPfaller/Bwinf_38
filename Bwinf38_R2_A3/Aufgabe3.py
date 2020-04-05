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
        root.title("Aufgabe3")
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
        if b[0] == a[0]:  # vertical
            if b[1] > a[1]:
                return float("Inf")
            else:
                return -float("Inf")
        val = (b[1] - a[1]) / (b[0] - a[0])
        if val == -0.0 or val == 0.0:  # horizontal
            return 0
        return val  # diagonally

    @staticmethod
    def get_min_dist(dist, queue):
        minimum = float("Inf")
        best = -1
        for v in queue:
            if dist[v] < minimum:
                minimum = dist[v]
                best = v
        return best

    def dijkstra(self, graph, start, target):
        queue = [start]

        visited = set()
        distances = {start: 0}
        parents = {start: None}
        while queue:
            vertex1 = self.get_min_dist(distances, queue)
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
        path = []
        cur = target
        while cur is not None:
            path.append(cur)
            cur = parents[cur]
        return distances, path

    # Erweiterung: Mehrere Ziele, die alle erreicht werden müssen

    def find_path(self, data, start, target, max_percentage):
        graph = self.connections.get_graph()
        distances, shortest_path = self.dijkstra(graph, start=target, target=start)  # distances relative to target
        max_dist = distances[start] * (1 + max_percentage / 100)
        queue = [start]
        parents = {start: [Node(node=start, parent=None, gradient=200, turns=0, distance=0)]}
        # dijkstra combined with finding least turns
        count = 0
        while queue:
            min_turns = []
            min_turn = float("Inf")
            for v in queue:
                if parents[v][0].get_turns() <= min_turn:
                    min_turn = parents[v][0].get_turns()
                    min_turns.append(v)
            max_distance = -1
            for v in min_turns:
                if distances[v] > max_distance:
                    max_distance = distances[v]
                    vertex1 = v
            queue.remove(vertex1)
            count += 1
            for vertex2, weight in graph[vertex1]:
                gradient = self.get_gradient(vertex1, vertex2)
                if vertex1 == start:
                    parents[vertex2] = [Node(vertex2, parents[start], gradient, 0, weight)]
                    queue.append(vertex2)
                else:
                    turns = (parents[vertex1][0].get_turns()) + 1
                    total_distance = float("Inf")
                    for e in parents[vertex1]:
                        if e.get_gradient() == gradient and e.get_distance() + weight + distances[vertex2] <= max_dist:
                            turns -= 1
                            total_distance = e.get_distance() + weight
                            best_node = e
                            break
                        elif total_distance > e.get_distance() + weight:
                            total_distance = e.get_distance() + weight
                            best_node = e
                    if best_node.get_distance() + weight + distances[vertex2] > max_dist:
                        continue
                    elif vertex2 not in parents.keys():
                        parents[vertex2] = [Node(vertex2, best_node, gradient, turns, total_distance)]
                        if vertex2 != target and vertex2 not in queue:
                            queue.append(vertex2)
                    else:
                        if turns == parents[vertex2][0].get_turns():
                            parents[vertex2].append(Node(vertex2, best_node, gradient, turns, total_distance))
                        elif turns < parents[vertex2][0].get_turns():
                            parents[vertex2] = [(Node(vertex2, best_node, gradient, turns, total_distance))]
                            if vertex2 != target and vertex2 not in queue:
                                queue.append(vertex2)
        # Output
        print(len(parents[target]))
        shortest = float("Inf")
        for i, e in enumerate(parents[target]):
            if e.get_distance() < shortest:
                shortest = e.get_distance()
                index = i

        print("Abbiegungen:")
        print(parents[target][index].get_turns())
        print("Distanz:")
        print(str(parents[target][index].get_distance()) + " (" + str(round(
            100 * parents[target][index].get_distance() / distances[start] - 100, 3)) + "% longer than the shortest path)")
        # create path
        cur = parents[target][index].get_parent()
        path = [target]
        while type(cur) != list:
            path.append(cur.get_node())
            cur = cur.get_parent()
        print("Pfad:")
        print(path)
        path.append(start)
        return path

    # def show_maximal_graph(self, data, start, graph, distances, max_dist):
    #     queue = [start]
    #     visited = set()
    #     result = Graph()
    #     cost = {start: 0}
    #     parents = {start: None}
    #     while queue:
    #         vertex1 = self.get_min_dist(cost, queue)
    #         queue.remove(vertex1)
    #         if vertex1 not in visited:
    #             visited.add(vertex1)
    #             for vertex2, weight in graph[vertex1]:  # weight := distance between the two vertices
    #                 if vertex2 in visited:
    #                     continue
    #                 # Updating distance if distance isn't set yet or the distance is shorter than the previous distance
    #                 if cost.get(vertex2, None) is None or cost.get(vertex1) + weight < cost.get(vertex2):
    #                     cost[vertex2] = cost.get(vertex1) + weight
    #                     parents[vertex2] = vertex1
    #                     queue.append(vertex2)
    #
    #     for v1 in graph.keys():
    #         for v2, weight in graph[v1]:
    #             if v1 in cost:
    #                 if cost.get(v1, None) + distances[v2] + weight <= max_dist:
    #                     result.add_edge(v1, v2, weight)
    #
    #     return result.get_graph()


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
result = s.find_path(d, d.start, d.target, percent)

print('In ' + str((time.time() - time1) * 1000) + ' Milliseconds (with file reading, without graphics)')

# graphical output
d.draw_path(result)
d.finish()
