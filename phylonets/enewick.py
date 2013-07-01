#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import re

import pyparsing
from pyparsing import Combine, Optional, Literal, CaselessLiteral
from pyparsing import Word, alphanums, alphas, alphas8bit, nums
from pyparsing import Group, Forward

from networkx.algorithms.traversal.depth_first_search import dfs_preorder_nodes

import networkx as nx

import cluster_networks

cvtInt = lambda s,l,toks: int(toks[0])
cvtReal = lambda s,l,toks: float(toks[0])

# http://www.trex.uqam.ca/index.php?action=newick

def make_enewick_parser():
    # atoms
    lparen    = Literal("(").suppress()
    rparen    = Literal(")").suppress()
    colon     = Literal(":").suppress()
    #semicolon = Literal(";").suppress()
    comma     = Literal(",").suppress()
    point     = Literal(".")
    e         = CaselessLiteral("E")
    sharp     = Literal("#").suppress()

    # terminal
    name    = Word(alphanums + alphas8bit \
                   + "_" + "-" + "." + "+" + "&" + "/" + "~" \
                   +  "{" + "}" + "*" + "'" + '"' + '\\' + '?')
    string  = Word(alphas)
    fnumber = Combine(
        Word("+-"+nums, nums) +
        Optional(point + Optional(Word(nums))) +
        Optional(e + Word("+-"+nums, nums))
        ).setParseAction(cvtReal)
    number = Combine(
        Word(nums)).setParseAction(cvtInt)

    label = \
        Optional(name).setResultsName("label") + \
        Optional(
            sharp +
            Optional(string).setResultsName("type") +
            number.setResultsName("tag")
            ) + \
        Optional(colon + fnumber).setResultsName("length")

    subtree = Forward()
    subtreelist = Forward()
    subtree << \
    Group(((lparen + subtreelist + rparen).setResultsName("subtree") |
           label
           ) + Optional(label)
          )
    subtreelist << subtree + Optional(comma + subtreelist)

    tree = subtree + Word(";").suppress()

    return tree.parseString


class MalformedNewickException(Exception):
    """
    Raised when creating a new network from a malformed eNewick string.
    """
    pass

def enewick_to_digraph(s):
    try:
        parsed = make_enewick_parser()(s)[0]
    except pyparsing.ParseException:
        raise MalformedNewickException("Malformed eNewick string")
    g = nx.DiGraph()
    _walk(g, parsed)
    # is_leaf = lambda x: not g.successors(x)
    # dfs = lambda x: dfs_preorder_nodes(g, x)
    trans_leafs = {}
    # remove the initial «#»
    for leaf in cluster_networks.get_leaf_nodes(g):
        trans_leafs[leaf] = re.sub("#", "", leaf)
    g = nx.relabel_nodes(g, trans_leafs)
    return g

def enewick_to_phylonet(s):
    g = enewick_to_digraph(s)
    g = cluster_networks.calc_hybrid(g)
    return g

def enewick_graph_cluster_hard(g):
    """
    Filter the hard clusters of the graph that are really inputed by
    the user. This means to remove all the _{} nodes.
    """
    return [n for n in g.nodes() if not str(n)[0] == '_']

def _generate_new_id(G):
    """
    Helper to generate labels in case the input is not complete.
    """
    return '_{}'.format(len(G.nodes()) + 1)

def _walk(G, parsed):
    if not isinstance(parsed, pyparsing.ParseResults):
        return
    if 'tag' in parsed:
        label = '#{}'.format(parsed['tag'])
    elif 'label' in parsed:
        label = parsed['label']
    else:
        label = _generate_new_id(G)
    G.add_node(label)
    for child in parsed:
        child_label = _walk(G, child)
        if child_label:
            G.add_edge(label, child_label)
    return label
