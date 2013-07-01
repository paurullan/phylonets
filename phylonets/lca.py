#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

from itertools import chain, groupby
from operator import itemgetter

import networkx as nx

"""
The module might be a little confusing but it implements LCSA and LCA, being
the strict selection parametric.
"""

def CSA(G, u, v, root=None):
    return CxA(G, u, v, root, func=_get_strict_path)

def CA(G, u, v, root=None):
    return CxA(G, u, v, root, func=_get_path)

def CxA(G, u, v, root=None, func=None):
    if not G.nodes():
        raise nx.NetworkXPointlessConcept("No on empty graphs")
    root = root if root else _get_root(G)
    if root not in G:
        raise nx.NetworkXPointlessConcept("Root must be in graph")
    if len(G.predecessors(root)) != 0:
        raise nx.NetworkXPointlessConcept("Root cannot have predecessors")
    path_v = func(G, node=v, root=root)
    path_u = func(G, node=u, root=root)
    csa = path_v.intersection(path_u)
    return csa

def _get_strict_path(G, node, root):
    """
    Get the individual CSA: take all the paths to the root and check that every node is in all them.
    """
    if node == root:
        return set([root, ])
    paths = nx.all_simple_paths(G=G, source=root, target=node)
    paths_set = [set(p) for p in paths]
    if not paths_set:
        raise nx.NetworkXError("Only for rooted graphs")
    nodes = paths_set[0].intersection(*paths_set)
    return nodes

def _get_path(G, node, root):
    """
    Get the individual CSA: take all the paths to the root and check that every node is in all them.
    """
    if node == root:
        return set([root, ])
    paths = nx.all_simple_paths(G=G, source=root, target=node)
    if not paths:
        raise nx.NetworkXError("Only for rooted graphs")
    return set(chain.from_iterable(paths))

def _get_root(G):
    roots = [n for n in G.nodes_iter() if not G.predecessors(n)]
    if len(roots) < 1:
        raise nx.NetworkXPointlessConcept("Root must be in graph")
    elif len(roots) > 1:
        raise nx.NetworkXPointlessConcept("Single rooted graph")

    assert len(roots) == 1, "only one root in the graph"
    root = roots[0]
    return root

def LCA(G, u, v, root=None):
    """Return a list of the least common ancestors"""
    return LCxA(G, u, v, root, CxA=CA)

def LCSA(G, u, v, root=None):
    lcsa = LCxA(G, u, v, root, CxA=CSA)
    assert len(lcsa) == 1, "LCSA is strictly one"
    return lcsa[0]

def LCxA(G, u, v, root=None, CxA=None):
    if not G.nodes():
        raise nx.NetworkXPointlessConcept("No on empty graphs")
    root = root if root else _get_root(G)
    cxa = CxA(G, u, v, root)
    if not cxa:
        return None
    if root not in cxa:
        raise nx.NetworkXError("the root has to be a CA")
    if len(cxa) == 1:
        return [cxa.pop()]
    elif len(cxa) == 2:
        cxa.remove(root)
        return [cxa.pop()]
    cxa.remove(root)

    # it is not for the distance but, being the CA a subgraf, those
    # nodes that are leafs.
    lcsa = []
    for node in cxa:
        succs = G.successors(node)
        if not any([succ in cxa for succ in succs]):
            lcsa.append(node)
    return lcsa


def is_strict_ancestor(G, dest, strict, root):
    return strict in CSA(G, u=dest, v=strict, root=root)
