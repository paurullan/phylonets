#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import unittest

import logging
log = logging.getLogger(__name__)

import networkx as nx

from lca import CSA, LCSA, LCA
from lca import _get_root

from cluster_networks import construct

class TestLCSA(unittest.TestCase):

    def setUp(self):
        """
        Simple graph for testing.
        1
        |
        2
        |
        3
        | \
        4  5
        |\
        6 7
        """
        self.G = nx.DiGraph()
        self.G.add_edges_from([
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 6),
            (3, 5),
            (4, 7),
        ])

    def test_empty_graph_csa(self):
        g = nx.DiGraph()
        u, v = None, None
        self.assertRaises(nx.NetworkXPointlessConcept,
                          CSA, g, u, v)

    def test_empty_graph_lcsa(self):
        g = nx.DiGraph()
        u, v = None, None
        self.assertRaises(nx.NetworkXPointlessConcept,
                          LCSA, g, u, v)


    def test_one(self):
        u, v = 1, 2
        result = LCSA(self.G, u, v)
        gold = 1
        self.assertEqual(result, gold)

    def test_aginst_root(self):
        root = 1
        for v in [2, 3, 4, 5, 6, 7]:
            self.assertEqual(LCSA(self.G, root, v), root)

    def test_two(self):
        u, v = 2, 4
        result = LCSA(self.G, u, v)
        gold = 2
        self.assertEqual(result, gold)

    def test_three(self):
        u, v = 4, 5
        result = LCSA(self.G, u, v)
        gold = 3
        self.assertEqual(result, gold)

    def test_four(self):
        u, v = 2, 7
        result = LCSA(self.G, u, v)
        gold = 2
        self.assertEqual(result, gold)

    def test_five_csa(self):
        u, v = 6, 7
        result = CSA(self.G, u, v)
        gold = [1, 2, 3, 4, ]
        self.assertItemsEqual(result, gold)

    def test_five(self):
        u, v = 6, 7
        result = LCSA(self.G, u, v)
        gold = 4
        self.assertEqual(result, gold)

    def test_six(self):
        u, v = 6, 5
        result = LCSA(self.G, u, v)
        gold = 3
        self.assertEqual(result, gold)


class TestGetRoot(unittest.TestCase):

    def setUp(self):
        self.G = nx.DiGraph()

    def test_one(self):
        self.G.add_edges_from([
            (1, 2),
        ])
        root = _get_root(self.G)
        gold = 1
        self.assertEqual(root, gold)

    def test_two(self):
        self.G.add_edges_from([
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 6),
            (3, 5),
            (4, 7),
        ])
        root = _get_root(self.G)
        gold = 1
        self.assertEqual(root, gold)

    def test_no_root(self):
        self.G.add_edges_from([
            (1, 2),
            (2, 1),
        ])
        self.assertRaises(nx.NetworkXPointlessConcept,
                          _get_root, self.G)

    def test_multiple_roots(self):
        self.G.add_edges_from([
            (1, 3),
            (2, 3),
        ])
        self.assertRaises(nx.NetworkXPointlessConcept,
                          _get_root, self.G)

class TestGraph(unittest.TestCase):
    """
     R = 1, 2, 3, 4, 5
      |              \
    (1, 2, 3)   (2, 3, 4, 5)
      |      \    /      \
     (1, 2)  (2, 3)h   (3, 4, 5)
      |  \      |       /      \
     (1,) \  (2, 3)  (3, 4)   (5,)
           \  /   \  /   |
           (2h,) (3h,)  (4,)
            |       |
           (2,)    (3,)
    """

    def setUp(self):
        clusters = [(1, 2), (2, 3), (3, 4),
                    (3, 4, 5), (1, 2, 3),
                    (2, 3, 4, 5)]
        self.root = "1,2,3,4,5"
        self.G = construct(clusters)


    def test_against_root(self):
        for v in self.G.nodes():
            self.assertEqual(LCSA(self.G, self.root, v), self.root)

    """
    Because of the form of the graph, the CSA and LCSA of both nodes
    (2, ) and (3, ) against any node is only the root.
    """
    def test_against_two(self):
        node = "2"
        nodes = self.G.nodes()
        nodes.remove("2")
        nodes.remove("2h")
        self.assertEqual(LCSA(self.G, node, "2", ), "2")
        self.assertEqual(LCSA(self.G, node, '2h',), '2h')
        for v in nodes:
            self.assertEqual(LCSA(self.G, node, v), self.root)

    def test_against_three(self):
        node = "3"
        nodes = self.G.nodes()
        nodes.remove("3")
        nodes.remove("3h")
        self.assertEqual(LCSA(self.G, node, "3", ), "3")
        self.assertEqual(LCSA(self.G, node, '3h',), '3h')
        for v in nodes:
            self.assertEqual(LCSA(self.G, node, v), self.root)

    def test_four(self):
        u, v = "1", "3,4,5"
        result = LCSA(self.G, u, v)
        self.assertEqual(result, self.root)

    def test_hybrids(self):
        u, v = '2h', '3h'
        gold = self.root
        result = LCSA(self.G, u, v)
        self.assertEqual(result, gold)

    def test_one_to_five(self):
        u, v = '1', '5'
        result = LCSA(self.G, u, v)
        self.assertEqual(result, self.root)

    def test_four_to_five(self):
        u, v = "4", "5"
        gold = "3,4,5"
        result = LCSA(self.G, u, v)
        self.assertEqual(result, gold)


class TestLCA(unittest.TestCase):
    """Different class for the LCA, where we get a list"""

    def setUp(self):
        """
        Simple graph for testing.
        1
        |
        2
        |
        3
        | \
        4  5
        |\
        6 7
        """
        self.G = nx.DiGraph()
        self.G.add_edges_from([
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 6),
            (3, 5),
            (4, 7),
        ])

    def test_empty_graph_csa(self):
        g = nx.DiGraph()
        u, v = None, None
        self.assertRaises(nx.NetworkXPointlessConcept,
                          CSA, g, u, v)

    def test_empty_graph_lcsa(self):
        g = nx.DiGraph()
        u, v = None, None
        self.assertRaises(nx.NetworkXPointlessConcept,
                          LCA, g, u, v)


    def test_one(self):
        u, v = 1, 2
        result = LCA(self.G, u, v)
        gold = [1]
        self.assertEqual(result, gold)

    def test_aginst_root(self):
        """The LCA returns a list"""
        root = 1
        for v in [2, 3, 4, 5, 6, 7]:
            self.assertEqual(LCA(self.G, root, v), [root])

    def test_two(self):
        u, v = 2, 4
        result = LCA(self.G, u, v)
        gold = [2]
        self.assertEqual(result, gold)

    def test_three(self):
        u, v = 4, 5
        result = LCA(self.G, u, v)
        gold = [3]
        self.assertEqual(result, gold)

    def test_four(self):
        u, v = 2, 7
        result = LCA(self.G, u, v)
        gold = [2]
        self.assertEqual(result, gold)

    def test_five_csa(self):
        u, v = 6, 7
        result = CSA(self.G, u, v)
        gold = [1, 2, 3, 4, ]
        self.assertItemsEqual(result, gold)

    def test_five(self):
        u, v = 6, 7
        result = LCA(self.G, u, v)
        gold = [4]
        self.assertEqual(result, gold)

    def test_six(self):
        u, v = 6, 5
        result = LCA(self.G, u, v)
        gold = [3]
        self.assertEqual(result, gold)
