#!/usr/bin/env python3
import numpy as np
import unittest, random, itertools
from queue import PriorityQueue

G1 = [{2:1}, {2:1}, {3:1, 7:1}, {5:1}, {5:1}, {6:1}, {}, {5:1}]


def get_undirected_graph(G):
    H = [set() for u in G]
    for u, V in enumerate(G):
        for v in V:
            H[u].add(v)
            H[v].add(u)
    return H

# def prim(G,s):
#     distance = np.array([1000]*len(G))
#     predecessor = -np.ones_like(G)
#     q = PriorityQueue()
#     distance[s] = 0
#     q.buildHeap([(distance[vi],v) for vi, v in enumerate(G)])
#     while not q.empty():
#         du, u = q.get()
#         for v in u.keys():
#             newCost = currentVert.getWeight(nextVert)
#             if nextVert in q and newCost<nextVert.getDistance():
#                 nextVert.setPred(currentVert)
#                 nextVert.setDistance(newCost)
#                 q.decreaseKey(nextVert,newCost)

# prim(G1,0)

print(get_undirected_graph(G1))