import collections
from collections import defaultdict


class Graph:

    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u_tuple, v_tuple, w):
        self.graph[u_tuple].append((v_tuple, w))
        #self.graph[v_tuple].append((u_tuple, w))

    def get_graph(self):
        return self.graph


filename = "Beispiel0.txt"

#   Read Data
file = open(filename, "r")

vertices = []
for line, val in enumerate(file.read().split()):
    if line == 0:
        size = int(val)
        grid = [[0 for col in range(size)] for row in range(size)]
    elif line == 1:
        robot = tuple(val.split(","))
        vertices.append((int(robot[0]) - 1, int(robot[1]) - 1, int(robot[2])))
        robot = (int(robot[1]) - 1, int(robot[0]) - 1, int(robot[2]))
        grid[robot[0]][robot[1]] = robot[2]
    elif line == 2:
        pass
    else:
        battery = tuple(val.split(","))
        vertices.append((int(battery[0]) - 1, int(battery[1]) - 1, int(battery[2])))
        grid[int(battery[1]) - 1][int(battery[0]) - 1] = int(battery[2])

file.close()

graph = Graph()


def manhattan_distance(x, y):
    return sum(abs(a - b) for a, b in zip(x, y))


for v1 in vertices:
    for v2 in vertices:
        if manhattan_distance((v1[0], v1[1]), (v2[0], v2[1])) <= v1[2] and v1 != v2:
            graph.add_edge((v1[0], v1[1]), (v2[0], v2[1]), v1[2])


def is_connected():
    visited = [False] * len(vertices)

    visited = depth_first_search(vertices[0], graph, visited)

    for b in visited:
        if not b:
            return False
    return True


def depth_first_search(vertex1, graph, visited):

    visited[vertex1] = True

    for vertex2 in graph[vertex1]:
        if not visited[vertex2]:
            depth_first_search(vertex2, graph, visited)

    return visited

# TODO: With Manhattan distance
# for i, v1 in enumerate(vertices):
#     if i == len(vertices) - 1:
#         break
#     index = i + 1
#     v2 = vertices[index]
#     while v2[0] < v1[0] + v1[2] and v2[1] < v2[1] + v1[2]:
#         if manhattan_distance((v1[0], v1[1]), (v2[0], v2[1])) <= v1[2]:
#             graph.add_edge((v1[0], v1[1]), (v2[0], v2[1]), v1[2])
#         if index == len(vertices) - 1:
#             break
#         index += 1
#         v2 = vertices[index]
#
#     if i == 0:
#         continue
#     index = i - 1
#     v2 = vertices[index]
#     while v2[0] > v1[0] - v1[2] and v2[1] > v1[0] - v1[2] and index > 0:
#         if manhattan_distance((v1[0], v1[1]), (v2[0], v2[1])) <= v1[2]:
#             graph.add_edge((v1[0], v1[1]), (v2[0], v2[1]), v1[2])
#         if index == 0:
#             break
#         index -= 1
#         v2 = vertices[index]


print(graph.get_graph())
print(vertices)
for e in grid:
    print(e)
