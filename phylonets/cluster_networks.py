#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division

import operator
from itertools import chain

import copy

from logging import getLogger
log = getLogger(__name__)

import networkx as nx
from networkx.utils.misc import flatten

from hasse import Hasse
from lca import LCA, is_strict_ancestor

# from redis_cache import cache_it, SimpleCache
# class MultiSessionCache(SimpleCache):
#     key_str = "multisession-cache"

#     def make_key(self, key):
#         return MultiSessionCache.key_str + "-" + str(key)

#     def get_set_name(self):
#         return MultiSessionCache.key_str

# my_cache = MultiSessionCache(hashkeys=True)
# @cache_it(cache=my_cache)


def construct(clusters):
    if len(clusters) == 1 and not clusters[0]:
        return nx.DiGraph()
    # the first net is the created from the Hasse, the second the real hybrid
    net = network(Hasse(clusters))
    hybrid = calc_hybrid(net)
    graph = relabel_graph(hybrid)
    return graph

def network(edge_list):
    """
    Alias for creating a graph from a list of edges
    """
    G = nx.DiGraph()
    G.add_edges_from(edge_list)
    return G

def clean_graph(G):
    """
    Streams and cleans a graph that has become polluted from transformations
    of the tree child process. Not pure, removes in place.
    """
    def _may_go(G, n):
        return G.in_degree(n) == 1 and G.out_degree(n) == 1

    candidates = [n for n in G.nodes() if _may_go(G, n)]
    if not candidates:
        return G
    else:
        node = candidates[0]
        # let's remove the node and change the in-out
        assert(len(G.predecessors(node)) == 1)
        assert(len(G.successors(node)) == 1)
        in_node = G.predecessors(node)[0]
        out_node = G.successors(node)[0]
        G.add_edge(in_node, out_node, group=1)
        G.remove_node(node)
        return clean_graph(G)

def calc_hybrid(G):
    """
    Gets a network, looks for all nodes that have multiple parents and makes
    the hybrid network.
    """
    for h in hybrid_nodes(G):
        preds = G.predecessors(h)
        new_node = str(h) + 'h'
        G.add_edge(new_node, h)
        for predecessor in preds:
            G.remove_edge(predecessor, h)
            G.add_edge(predecessor, new_node)
    return G

def is_treechild(G):
    """ We take all the nodes but the root. """
    non_leaf_nodes = get_non_leaf_nodes(G)
    return all([has_tree_child(G, n) for n in non_leaf_nodes])

def hybridization_degree(G):
    edges, nodes = len(G.edges()), len(G.nodes())
    return edges - nodes + 1

def get_root_nodes(G):
    return [n for n in G.nodes() if len(G.predecessors(n)) == 0]

def get_leaf_nodes(G):
    return [n for n in G.nodes() if len(G.successors(n)) == 0]

def get_non_leaf_nodes(G):
    return [n for n in G.nodes() if len(G.successors(n)) > 0]

def has_tree_child(G, n):
    return any([node_tree(G, child) for child in G.successors(n)])

def hybrid_nodes(G):
    return [n for n in G.nodes() if is_hybrid(G, n)]

def tree_nodes(G):
    hybrids = hybrid_nodes(G)
    return [n for n in G.nodes() if n not in hybrids]

def is_hybrid(G, n):
    return G.in_degree(n) > 1

def node_tree(G, n):
    return G.in_degree(n) <= 1



def _make_set(leaf_list):
    return set(zip(*sorted(leaf_list)))

def embedded_trees(G):
    """Calculate the embedded trees in the network."""
    if not hybrid_nodes(G):
        yield G
    else:
        h = hybrid_nodes(G)[0]
        preds = G.predecessors(h)
        assert len(preds) > 1, "Always and at least two predecessors"
        assert len(G.successors(h)) >= 1, "At least one successor on hybrids"
        assert len(G.successors(h)) == 1, "Only one successor on hybrids"
        successor = G.successors(h)[0]
        for predecessor in preds:
            g = G.copy()
            g.remove_node(h)
            g.add_edge(predecessor, successor,  name="", group=1)
            g = clean_graph(g)
            for val in embedded_trees(g):
                yield val

def check_cluster(clusters):
    """
    Checks if the C_soft(N) == C_hard(N) of a network.
    """
    G = construct(clusters)
    return cluster_hard(G) == cluster_soft(G)

def _leaves_from(G, node):
    dfs = nx.algorithms.traversal.dfs_preorder_nodes
    nodes = dfs(G, node)
    leafs = get_leaf_nodes(G)
    return {leaf for leaf in nodes if leaf in leafs}

def relabel_graph(G):
    """
    Recalculates the graph in the hard-accessibility way.
    """
    trans_leafs = {}
    for leaf in get_leaf_nodes(G):
        leaf_str = "".join(map(str, leaf))
        trans_leafs[leaf] = leaf_str
    G = nx.relabel_nodes(G, trans_leafs)

    trans = {}
    for node in get_non_leaf_nodes(G):
        leafs = _leaves_from(G, node)
        new_name = ",".join(sorted(flatten(leafs)))
        if is_hybrid(G, node):
            new_name += 'h'
        tr = {node: new_name, }
        trans.update(tr)
    g = nx.relabel_nodes(G, trans, copy=True)
    g.name = "phylonet"
    return g

# @cache_it(cache=my_cache)
def cluster_hard(G_orig):
    G = clean_graph(G_orig.copy())
    G = relabel_graph(G)
    return tree_nodes(G)

def potential_number_of_calls(G):
    """
    The potential number of calls for a soft_cluster is the product of the
    many hybrid nodes by their input level.
    """
    H = hybrid_nodes(G)
    return reduce(operator.mul, [len(G.predecessors(h)) for h in H], 1)

def cluster_soft(G):
    """
    Calculate the softcluster of the graph. It is important to take into
    account that we cannot just remove one of the predecessors since it will
    be an usual case were an hybrid node has three predecessors.
    """
    clusters = [cluster_hard(tree) for tree in embedded_trees(G)]
    return list(set(chain.from_iterable(clusters)))

#########
## remove edge: PhyloRec algorithm
def _test_individual_v(G, edge, v, root):
    """
    Actual test for the edge removal. For a single v.
    """
    u, h = edge
    if u == v:
        raise nx.NetworkXError("Wrongly passed the edge and removable node")
    ## Aquí és on cal corregir el comportament del llevar aresta
    ws = LCA(G, u, v, root)
    wi = G.successors(h)
    assert len(wi) == 1, "Hybrids must have only one child"
    # w1 = wi[0]
    leaves = lambda x: _leaves_from(G, x)
    leaves_u = leaves(u)
    leaves_v = leaves(v)
    def check_reticular_paths(u, ws):
        paths = lambda w: nx.all_simple_paths(G, source=w, target=u)
        for w in ws:
            if any([single_path(uis, u, w) for uis in paths(w)]):
                return True
        return False

    def single_path(uis_orig, u, w):
        uis = copy.deepcopy(uis_orig)
        uis.remove(u)
        uis.remove(w)
        for ui in uis:
            leaves_ui = leaves(ui)
            xs = leaves_ui - leaves(u)
            if any([is_strict_ancestor(G, x, ui, root) for x in xs]):
                return False
        return True

    # 1. stricts from ui
    if not check_reticular_paths(u, ws):
        return False
    # 2. stricts from vi
    if not check_reticular_paths(v, ws):
        return False
    # 3. intersection w - u - v
    for w in ws:
        leaves_out = leaves(w) - leaves_v - leaves_u
        for leaf in leaves_out:
            if is_strict_ancestor(G, dest=leaf, strict=w, root=root):
                return False
    # and we are happy to go.
    return True

def is_problematic(G, node):
    succs = G.successors(node)
    return all([is_hybrid(G, n) for n in succs])

def remove_edge(G, edge):
    """
    Calc if an edge is removable as shown in Llabrès (2013).

    Take into account that the removable edge must be one of the calculated,
    the u will be the from_node and the to_node the hybrid node.
    The different vs will be all the other parents of h.

    """
    if not G.nodes():
        raise nx.NetworkXPointlessConcept(
            "Cannot remove edge from empty graph")
    if not edge:
        raise TypeError("Need an edge")
    if tuple(edge) not in removable_edges(G):
        raise nx.NetworkXError("Wrong possible edge")
    try:
        root = get_root_nodes(G)[0]
    except IndexError:
        raise nx.NetworkXPointlessConcept("The graph has to be rooted")
    preds = lambda h: G.predecessors(h)
    problematics = problematic_treechild_nodes(G)
    u, h = edge
    vs = [v for v in problematics if v in preds(h) and v != u]
    return all([_test_individual_v(G, edge, v, root) for v in vs])


def removable_edges(G):
    """
    Search for the potential removable edges.
    1. look for a node with all children hybrids
    2. look for the fathers of these hybrids that have a node
    3. take the edges that connect those nodes
    4. The edges from the hybrids are not removable
    """
    if not G.edges():
        return []
    def _individual_removable(problematic_node, problematics):
        children = G.successors(problematic_node)
        edges_parents = []
        for child in children:
            for parent in G.predecessors(child):
                if parent not in problematics:
                    edges_parents.append((parent, child))
        return edges_parents

    problematics = problematic_treechild_nodes(G)
    edges = [_individual_removable(node, problematics) for node in problematics]
    edges = set(chain.from_iterable(edges))
    return edges

def problematic_treechild_nodes(G):
    """
    Look for a node with all children hybrids
    """
    non_leafs = get_non_leaf_nodes(G)
    return [n for n in non_leafs if is_problematic(G, n) ]

# @cache_it(cache=my_cache)
def remove_edge_naive(G, edge):
    """
    The naïve approach to remove an edge is to search if the soft would be the
    same before and after removing it.
    """
    if not edge:
        raise TypeError("Need an edge")
    if not G.nodes():
        raise nx.NetworkXPointlessConcept(
            "Cannot remove edge from empty graph")
    soft = cluster_soft(G)
    g = G.copy()
    u, v = edge
    g.remove_edge(u=u, v=v)
    soft2 = cluster_soft(g)
    return soft == soft2

def check_problematic_row(G):
    """
    Look for the branching optimization for the case were a series of
    problematic nodes are chained so there are no tree nodes connected
    to them. Returns True in case there is a problematic row.

    A single level of look-up is enought since we look for all nodes.
    """
    problematics = problematic_treechild_nodes(G)
    trees = set(tree_nodes(G)) - set(problematics)
    def _access(prob):
        outs = [e[1] for e in G.out_edges(prob)]
        nodes = {e[0] for out in outs for e in G.in_edges(out)}
        return nodes
    for node in problematics:
        visited = set()
        pendings = _access(node)
        while pendings:
            p = pendings.pop()
            visited.add(p)
            if p in trees:
                break
            else:
                for accessible in _access(p):
                    if accessible not in visited:
                        pendings.add(accessible)
        if not pendings:
           return True
    return False

def construct_treechild(G):
    if is_treechild(G):
        return []
    if check_problematic_row(G):
        return []
    results = {}
    _make_treechild(G, results)
    # calls = [0,]
    # _make_treechild(G, results, level=0, calls=calls)
    # log.debug("calls:\t{}".format(calls[0]))
    # log.debug("tree-childs: \t {}".format(len(results)))
    return results.values()

def is_origin_problematic(G, edge):
    u, v = edge
    return is_problematic(G, u)

def _g_key(g):
    return tuple(sorted(cluster_hard(g)))

# def _make_treechild(G, results, level=0, calls=[]):
def _make_treechild(G, results):
    """
    Try to construct the tree-child versions of the network.
    Take into account that this generates the _new_ versions of the graph:
    if the graph is already tree child it will yield empty.
    """
    # calls[0] += 1
    # call = calls[0]
    # if call % 100 == 0:
    #     log.debug(call)
    # log.debug("level \t {} \t {}".format("-"*level, level))
    # log.debug("")
    if is_treechild(G):
        # log.debug("\t \t \t \t network found")
        results[_g_key(G)] = G
        return
    else:
        for edge in removable_edges(G):
            if remove_edge(G, edge):
                g = G.copy()
                u, v = edge
                g.remove_edge(u, v)
                clean_graph(g)
                # _make_treechild(g, results, level+1, calls)
                _make_treechild(g, results)
