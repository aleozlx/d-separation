#!/usr/bin/env python3
from collections import deque
import numpy as np
import unittest, random, itertools

def bfs(G, a = None):
    """ BFS traverse the connected component of a in G
    G: a directed graph
    a: root vertex """
    counter = itertools.count(1)
    visited = np.zeros_like(G).astype(bool)
    discover = -np.ones_like(G)
    predecessor = -np.ones_like(G)
    results = (discover, predecessor)

    if not G: # empty graph
        return results
    
    if a == None:
        a = random.choice(range(len(G)))

    queue = deque([a])
    discover[a] = next(counter)
    assert all([0<=u<len(G) for u in queue])

    while queue:
        u = queue.popleft()
        if not visited[u]:
            visited[u] = True
            if G[u]:
                discovered = np.array([[v, next(counter)] for v in G[u] if not visited[v]])
                queue.extend(discovered[:, 0])
                discover[discovered[:, 0]] = discovered[:, 1]
                predecessor[discovered[:, 0]] = u

    return results
