#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hasse import Hasse
import networkx as nx
import matplotlib.pyplot as plt

def case_one():
    c = [[1, 2], [1, 2, 3], ]
    return c

def case_two():
    c = [ [1, 2], [2, 3], [3, 4], [4, 5] ]
    return c

c = case_one()
c = case_two()
r = Hasse(c)
G = nx.DiGraph()
G.add_edges_from(r)
nx.draw(G)
plt.show()
