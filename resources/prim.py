#!/usr/bin/env python3
import numpy as np
import unittest, random, itertools
from heapq import heapify, heappush, heappop

G1 = [{2:1}, {2:1}, {3:1, 7:1}, {5:1}, {5:1}, {6:1}, {}, {5:1}]

class HeapQueue(list):
    def __init__(self, *args, **kargs):
        super(HeapQueue, self).__init__(*args, **kargs)
        self.index = {HeapQueue.item2vertex(i):i for i in self}
        self.__contains__ = self.index.__contains__
        heapify(self)

    @staticmethod
    def item2vertex(item):
        (_, (u, V)) = item
        return u

    def put(self, item):
        v = HeapQueue.item2vertex(item)
        if v in self.index:
            old_item = index.pop(v)
            old_item[1] = None
        heappush(self, item)
        self.index[v] = item

    def get(self):
        while 1:
            item = heappop(self)
            if not item[1]:
                continue
            del self.index[HeapQueue.item2vertex(item)]
            return item

    # def decreaseKey(self, vertex, weight):
    #     # TODO pos=?
    #     newitem = self[pos]
    #     while pos > 0:
    #         parentpos = (pos - 1) >> 1
    #         parent = self[parentpos]
    #         if cmp_lt(newitem, parent):
    #             self[pos] = parent
    #             pos = parentpos
    #             continue
    #         break
    #     self[pos] = newitem

def get_undirected_graph(G):
    H = [dict() for u in G]
    for u, V in enumerate(G):
        for v, d in V.items():
            H[u][v] = H[v][u] = d
    return H

def prim(G,s):
    distance = [1000]*len(G)
    predecessor = -np.ones_like(G)
    distance[s] = 0
    q = HeapQueue([[distance[u],(u,V)] for u, V in enumerate(G)])
    while q:
        (du, (u, V)) = q.get()
        # print('u', u)
        for v, duv in V.items():
            # print('v', v)
            if v in q and duv < distance[v]:
                predecessor[v] = u
                distance[v] = duv
                print('v', v)
                q.put([distance[v], (v, G[v])])
    return predecessor==-1
                # q.decreaseKey(v, weight)

print(prim(get_undirected_graph(G1),0))
# a = HeapQueue([(1,(3,dict())),(1,(2,dict())),(1,(7,dict())),(1,(5,dict())),(1,(0,dict()))])
# print(a)
# print(a.vset)
