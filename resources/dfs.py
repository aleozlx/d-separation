#!/usr/bin/env python3
import numpy as np
import unittest, random, itertools

def dfs(G, a = None, returns = 'dfa'):
    """ DFS traverse the connected component of a in G
    G: a directed graph
    a: root vertex """
    counter = itertools.count(1)
    visited = np.zeros_like(G).astype(bool)
    discover = -np.ones_like(G)
    finish = -np.ones_like(G)
    ancestor = -np.ones_like(G)
    results = {'d':discover, 'f':finish, 'a':ancestor}
    results = tuple([results[i] for i in returns])

    if not G: # empty graph
        return results
    
    if a == None:
        a = random.choice(range(len(G)))

    stack = [a]
    discover[a] = next(counter)
    assert all([0<=u<len(G) for u in stack])

    while stack:
        u = stack.pop()
        if u<0: # this is backtrack
            finish[-u-1] = next(counter)
            continue
        else:
            stack.append(-u-1)

        if not visited[u]:
            visited[u] = True
            if G[u]:
                discovered = np.array([[v, next(counter)] for v in G[u] if not visited[v]])
                stack.extend(reversed(discovered[:, 0]))
                discover[discovered[:, 0]] = discovered[:, 1]
                ancestor[discovered[:, 0]] = u

    return results
