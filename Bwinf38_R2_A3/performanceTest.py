from collections import defaultdict
from heapq import *
import time
import collections


def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))

    q, seen, mins = [(0,f,())], set(), {f: 0}
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: return (cost, path)
            for c, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))

    return float("inf")


def dijkstra2(edges, f, t):
    g = defaultdict(list)
    for l, r, c in edges:
        g[l].append((c, r))

    visited = []
    queue = collections.deque([f])
    visited.append(f)

    while queue:
        vertex = queue.popleft()
        for w, neighbour in g[vertex]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)

    dist_to_target = defaultdict()
    parents = defaultdict()
    for e in visited:
        dist_to_target[e] = float("Inf")
        parents[e] = None

    dist_to_target[f] = 0
    for e in visited:
        for w, x in g[e]:
            if dist_to_target[e] + w < dist_to_target[x]:
                dist_to_target[x] = dist_to_target[e] + w
                parents[x] = e
    cur = t
    res = []
    while cur != None:
        cur = parents[cur]
        res.append(cur)

    return res, dist_to_target[t]


if __name__ == "__main__":
    edges = [
        ("A", "B", 7),
        ("A", "D", 5),
        ("B", "C", 8),
        ("B", "D", 9),
        ("B", "E", 7),
        ("C", "E", 5),
        ("D", "E", 15),
        ("D", "F", 6),
        ("E", "F", 8),
        ("E", "G", 9),
        ("F", "G", 11)
    ]

    time.sleep(3)
    count = 1000
    t1 = time.time()
    for i in range(count):
        print(dijkstra(edges, "A", "E"))
        dijkstra(edges, "F", "G")
        dijkstra(edges, "A", "E")
        dijkstra(edges, "F", "G")
        dijkstra(edges, "A", "E")
        dijkstra(edges, "F", "G")
    print(time.time() - t1)
    time.sleep(3)
    t1 = time.time()
    for i in range(count):
        dijkstra2(edges, "A", "E")
        dijkstra2(edges, "F", "G")
        dijkstra2(edges, "A", "E")
        dijkstra2(edges, "F", "G")
        dijkstra2(edges, "A", "E")
        dijkstra2(edges, "F", "G")
    print(time.time() - t1)