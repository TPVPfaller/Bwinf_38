from collections import defaultdict
import re
import math

class Data:

    def __init__(self, name):
        file = open(name, "r")
        self.connections = Graph()
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
        file.close()

    @staticmethod
    def calc_distance(tuple1, tuple2):
        return math.sqrt(math.pow((tuple2[0] - tuple1[0]), 2) + math.pow((tuple2[1] - tuple1[1]), 2))


class Graph:

    def __init__(self):
        self.graph = defaultdict(list)
        self.nodes = []

    def add_edge(self, u_tuple, v_tuple, w):
        self.graph[u_tuple].append((v_tuple, w))
        self.graph[v_tuple].append((u_tuple, w))

    def get_graph(self):
        return self.graph

    def get_length(self):
        return len(self.graph)

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
        self.nodes.append(data.start)
        self.sort(q)
        return self.nodes

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

    def a_star(self, d, start, target):
        dist = defaultdict()
        heuristic = defaultdict()
        parent = defaultdict(list)

        v = self.get_nodes(d)
        for i in range(0, self.get_length()):
            dist[v[i]] = float("Inf")
            parent[v[i]] = None
            heuristic[v[i]] = math.sqrt((v[i][0] - target[0])**2 + (v[i][1] - target[1])**2)
            print(v[i], heuristic[v[i]])
        dist[start] = 0
        parent[start] = start
        print(v)
        queue = v.copy()
        while queue:
            u = queue.pop()



        # states:   unknown = 0, in priority queue = 1, fully processed = 2

    def dijkstra(self, start, target):
        pass




d = Data("Beispiel0.txt")
d.connections.print()
d.connections.a_star(d, d.start, d.target)
#d.connections.dijkstra(d, d.start, d.target)