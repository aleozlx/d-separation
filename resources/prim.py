#!/usr/bin/env python3
import numpy as np
import unittest, random, itertools
from heapq import heapify

G1 = [{2:1}, {2:1}, {3:1, 7:1}, {5:1}, {5:1}, {6:1}, {}, {5:1}]


def get_undirected_graph(G):
    H = [dict() for u in G]
    for u, V in enumerate(G):
        for v,d in V.items():
            H[u][v] = H[v][u] = d
    return H

def prim(G,s):
    distance = [1000]*len(G)
    predecessor = -np.ones_like(G)
    distance[s] = 0
    q = heapify([(distance[u],(u,V)) for u, V in enumerate(G)])
    while not q.empty():
        (du, (u, V)) = q.get()
        print(u)
        for v, weight in V.items():
            newCost = weight
            if v in q.queue and newCost<distance[v]:
                predecessor[v] = u
                distance[v] = newCost
                q.decreaseKey(nextVert,newCost)

prim(get_undirected_graph(G1),0)
