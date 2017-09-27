#!/usr/bin/env python3
import os, sys
import numpy as np
import unittest, random, itertools

#     0
#     v
#   3<2>7
#   v ^
# 4>5 1
#   v
#   6

G1 = [set([2]), set([2]), set([3, 7]), set([5]), set([5]), set([6]), set(), set()]
_G1 = [set([2, 4]), set([2]), set([3, 7]), set([5]), set([5]), set([6]), set(), set()]

#     1<0
#     v v
# 7<4<3<2
#   v v
#   6<5
#     v
#     8

G2 = [set([1,2]), set([3]), set([3]), set([4,5]), set([6,7]), set([6,8]), set(), set(), set()]

def get_undirected_graph(G):
    H = [set() for u in G]
    for u, V in enumerate(G):
        for v in V:
            H[u].add(v)
            H[v].add(u)
    return H

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

def path_generator(G, a, b):
    """ Find all paths from a to b in directed graph G """
    assert all([0<=u<len(G) for u in [a,b]])
    path = []
    stack = [a]
    while stack:
        u = stack.pop()
        if u<0: # this is backtrack
            path.pop()
            continue
        else:
            stack.append(-1) # backtrack trap
            path.append(u)
            if u==b:
                yield path.copy()
                continue # not interested in any path circles back here
        stack.extend(G[u]-set(path))

def get_descendants(G, a):
    assert all([0<=u<len(G) for u in [a]])
    visited = set()
    stack = [a]
    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            stack.extend(G[u]-visited)
    return visited-set([a])


def dsep(G, a, b, C):
    """ Check whether a and b are d-separated wrt C, which would imply
        P(AB|C) = P(A|C)P(B|C) or P(A|BC) = P(A|C)
    G: r.v. dependence graph (a directed graph) 
    a,b: vertices in G representing random variables
    C: a set of conditional variables
    returns: d-separation between a and b """
    assert all([0<=u<len(G) for u in set([a,b])|C])
    assert a not in C and b not in C and a!=b
    for path in path_generator(get_undirected_graph(G), a, b):
        # detect d-connection
        # ref: https://www.andrew.cmu.edu/user/scheines/tutor/d-sep.html
        colliders = [(path[i], path[i] in G[path[i-1]]&G[path[i+1]]) for i in range(1, len(path)-1)]
        dconn = all([(
            (collider and ((get_descendants(G, v)|set([v]))&C)) or
            (not collider and v not in C))
                for v, collider in colliders])
        if dconn:
            return False
    else:
        return True

class UndirectedGraph(unittest.TestCase):
    def test_undirected_graph(self):
        for adj1, adj2 in zip(
                [set([2]), set([2]), set([0, 1, 3, 7]), set([2, 5]), set([5]), set([3, 4, 6]), set([5]), set([2])],
                get_undirected_graph(G1)):
            self.assertEqual(adj1, adj2)

class DSeparation(unittest.TestCase):
    def test_01(self):
        self.assertTrue(dsep(G1, 0, 3, set([2])))
    
    def test_02(self):
        self.assertFalse(dsep(G1, 0, 1, set([2])))

    def test_03(self):
        self.assertTrue(dsep(G1, 3, 4, set([2])))

    def test_04(self):
        self.assertFalse(dsep(G1, 3, 6, set([2])))

    def test_05(self):
        self.assertFalse(dsep(G1, 3, 5, set([2])))

    def test_06(self):
        self.assertTrue(dsep(G1, 3, 7, set([2])))

    def test_07(self):
        self.assertTrue(dsep(G1, 1, 6, set([2])))

    def test_08(self):
        self.assertTrue(dsep(G1, 1, 4, set([2])))

    def test_09(self):
        self.assertTrue(dsep(G1, 4, 7, set([2])))

    def test_10(self):
        for i,j in itertools.product(range(len(G1)), range(len(G1))):
            if i!=j and i!=6 and j!=6:
                self.assertFalse(dsep(G1, i, j, set([6])))

    def test_11(self):
        self.assertFalse(dsep(_G1, 1, 4, set([2])))

    def test_12(self):
        self.assertFalse(dsep(_G1, 1, 6, set([2])))

    def test_13(self):
        self.assertTrue(dsep(_G1, 1, 3, set([2])))

    def test_14(self):
        self.assertTrue(dsep(_G1, 6, 7, set([2])))

if __name__ == '__main__':
    # for p in path_generator(G1, 0, 6):
    #     print(p)
    unittest.main()
