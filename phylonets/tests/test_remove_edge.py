#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import unittest

import logging
log = logging.getLogger(__name__)

import networkx as nx

from cluster_networks import construct
from cluster_networks import is_treechild
from cluster_networks import remove_edge
from cluster_networks import removable_edges
from cluster_networks import problematic_treechild_nodes
from cluster_networks import construct_treechild

class TestRemoveEdgeMethods(unittest.TestCase):

    def setUp(self):
        clusters = [(1, 2), (2, 3), (3, 4),
                    (3, 4, 5), (1, 2, 3), (2, 3, 4, 5)]
        self.G = construct(clusters)

    def test_empty_graph(self):
        g = nx.DiGraph()
        edge = ((1, 2), (1,))
        self.assertRaises(nx.NetworkXPointlessConcept,
                          remove_edge, G=g, edge=edge)

    def test_no_edge(self):
        edge = None
        self.assertRaises(TypeError,
                          remove_edge, G=self.G, edge=edge)

    def test_problematic_treechild_empty(self):
        G = nx.DiGraph()
        node = problematic_treechild_nodes(G)
        gold = []
        self.assertItemsEqual(node, gold)

    def test_removable_edges_empty(self):
        empty = nx.DiGraph()
        edges = removable_edges(empty)
        self.assertItemsEqual(edges, [])

    def test_construct_treechild_empty(self):
        empty = nx.DiGraph()
        tcs = construct_treechild(empty)
        gold = []
        self.assertItemsEqual(tcs, gold)

    def test_construct_treechild_already_treechild(self):
        g = nx.DiGraph()
        g.add_edges_from([ ((1,), (2,)) ])
        self.assertTrue(is_treechild(g))
        tcs = construct_treechild(g)
        gold = []
        self.assertItemsEqual(tcs, gold)

class TestRemoveEdge(unittest.TestCase):

    def setUp(self):
        clusters = [(1, 2), (2, 3), (3, 4),
                    (3, 4, 5), (1, 2, 3), (2, 3, 4, 5)]
        self.G = construct(clusters)

    def test_treechild(self):
        self.assertFalse(is_treechild(self.G))

    def test_problematic_treechild(self):
        node = problematic_treechild_nodes(self.G)
        gold = ["2,3", ]
        self.assertItemsEqual(node, gold)

    def test_removable_edges(self):
        edges = removable_edges(self.G)
        gold = [ ("1,2", "2h"), ("3,4", "3h")]
        self.assertItemsEqual(edges, gold)

    def test_first_edge(self):
        edge = ("1,2", "2h")
        self.assertTrue(remove_edge(self.G, edge))

    def test_second_edge_cannot_remove(self):
        edge = ["3,4", "3h"]
        self.assertFalse(remove_edge(self.G, edge))

    def test_construct(self):
        tree_childs = construct_treechild(self.G)
        self.assertEqual(len(tree_childs), 1)
        graph_gold = self.G.copy()
        graph_gold.remove_edge(u="1,2", v='2h')
        graph_gold.remove_node('2h')
        graph_gold.remove_node("1,2")
        gold = [graph_gold, ]
        for tc, gg in zip(tree_childs, gold):
            self.assertItemsEqual(tc.nodes(), gg.nodes())


class TestRemoveEdgeSecondExample(unittest.TestCase):

    def setUp(self):
        clusters = [(1, 2), (3, 4), (4, 5),
                    (1, 2, 3), (3, 4, 5), (1, 2, 3, 4)]
        self.G = construct(clusters)

    def test_treechild(self):
        self.assertFalse(is_treechild(self.G))

    def test_problematic_treechild(self):
        node = problematic_treechild_nodes(self.G)
        gold = ["3,4"]
        self.assertItemsEqual(node, gold)

    def test_removable_edges(self):
        edges = removable_edges(self.G)
        gold = [ ("1,2,3", "3h"), ("4,5", "4h"),]
        self.assertItemsEqual(edges, gold)

    def test_left(self):
        edge = "1,2,3 3h".split()
        self.assertTrue(remove_edge(self.G, edge))

    def test_right(self):
        edge = ("4,5", '4h')
        self.assertTrue(remove_edge(self.G, edge))

    def test_left_cannot(self):
        """The edge is not in the network"""
        edge = ((3, 4), ('3h', ))
        self.assertRaises(nx.NetworkXError,
                          remove_edge, G=self.G, edge=edge)

    def test_right_cannot(self):
        """The edge is not in the network"""
        edge = [(3, 4), ('4h', )]
        self.assertRaises(nx.NetworkXError,
                          remove_edge, G=self.G, edge=edge)

    def test_construct(self):
        graph_gold_left = self.G.copy()
        graph_gold_left.remove_edge(u="1,2,3", v='3h')
        graph_gold_left.remove_node("1,2,3")
        graph_gold_left.remove_node("3h")
        graph_gold_right = self.G.copy()
        graph_gold_right.remove_edge(u="4,5", v="4h")
        graph_gold_right.remove_node("4,5")
        graph_gold_right.remove_node('4h')
        gold = [graph_gold_right, graph_gold_left, ]
        tree_childs = construct_treechild(self.G)
        self.assertEqual(len(tree_childs), 2)
        for tc, gg in zip(tree_childs, gold):
            self.assertItemsEqual(tc.nodes(), gg.nodes())


class TestRemoveEdgeThirdExample(unittest.TestCase):
    """This tree is interesting because we cannot remove any edge"""

    def setUp(self):
        clusters = [(1, 2), (2, 3, 4),
                    (4, 5), (2, 4), (1, 2, 3, 4)]
        self.G = construct(clusters)

    def test_treechild(self):
        self.assertFalse(is_treechild(self.G))

    def test_problematic_treechild(self):
        node = problematic_treechild_nodes(self.G)
        gold = ["2,4"]
        self.assertItemsEqual(node, gold)

    def test_removable_edges(self):
        edges = removable_edges(self.G)
        gold = [('1,2', '2h'), ('4,5', '4h'), ]
        self.assertItemsEqual(edges, gold)

    def test_all_edges(self):
        edges = removable_edges(self.G)
        for edge in edges:
            self.assertFalse(remove_edge(self.G, edge))

    def test_construct(self):
        tree_childs = construct_treechild(self.G)
        gold = []
        self.assertItemsEqual(tree_childs, gold)


class TestRemoveEdgeFourthExample(unittest.TestCase):
    """
    This tree is interesting because we cannot remove the first edge
    [ (2, 3), (3h,)] because of condition 3.
    """

    def setUp(self):
        clusters = [(1, 2, 3), (2, 3), (3, 4), (4, 5)]
        self.G = construct(clusters)

    def test_treechild(self):
        self.assertFalse(is_treechild(self.G))

    def test_problematic_treechild(self):
        node = problematic_treechild_nodes(self.G)
        gold = ["3,4", ]
        self.assertItemsEqual(node, gold)

    def test_removable_edges(self):
        edges = removable_edges(self.G)
        gold = [("2,3", "3h"), ("4,5", "4h")]
        self.assertItemsEqual(edges, gold)

    def test_all_edges(self):
        edges = removable_edges(self.G)
        for edge in edges:
            self.assertFalse(remove_edge(self.G, edge))

    def test_construct(self):
        tree_childs = construct_treechild(self.G)
        gold = []
        self.assertItemsEqual(tree_childs, gold)


class TestRemoveEdgeFithExample(unittest.TestCase):
    def setUp(self):
        clusters = [(2, 3), (3, 4), (4, 5), (1, 2, 3), (1,2,3,4)]
        self.G = construct(clusters)

    def test_treechild(self):
        self.assertFalse(is_treechild(self.G))

    def test_problematic_treechild(self):
        node = problematic_treechild_nodes(self.G)
        gold = ["3,4", ]
        self.assertItemsEqual(node, gold)

    def test_removable_edges(self):
        edges = removable_edges(self.G)
        gold = [("2,3", "3h"), ("4,5", "4h")]
        self.assertItemsEqual(edges, gold)

    def test_all_edges(self):
        edges = removable_edges(self.G)
        for edge in edges:
            self.assertFalse(remove_edge(self.G, edge))

    def test_construct(self):
        tree_childs = construct_treechild(self.G)
        gold = []
        self.assertItemsEqual(tree_childs, gold)
