#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import unittest

from networkx.algorithms.isomorphism import GraphMatcher

from cluster_networks import construct
from cluster_networks import cluster_hard

from enewick import enewick_to_digraph
from enewick import enewick_to_phylonet

class TestWeb(unittest.TestCase):

    def test_one(self):
        text = "((MOUSE,(HUMAN,RAT)),CIOIN);"
        enewick_graph = enewick_to_digraph(text)
        self.assertEqual(len(enewick_graph.nodes()), 7)
        enewick_graph = enewick_to_phylonet(text)
        self.assertEqual(len(enewick_graph.nodes()), 7)
        clusters = [(1, 2, 3), (2, 3), (4,)]
        gold = construct(clusters)
        GM = GraphMatcher(enewick_graph, gold)
        self.assertTrue(GM.is_isomorphic())
        gold_hard = [
             'CIOIN,HUMAN,MOUSE,RAT',
             'CIOIN', 'HUMAN', 'MOUSE', 'RAT',
             'HUMAN,MOUSE,RAT',
             'HUMAN,RAT',
            ]
        hard = cluster_hard(enewick_graph)
        self.assertEqual(len(hard), 7)
        self.assertItemsEqual(hard, gold_hard)

    def test_two(self):
        text = "((4, 5#1)2, (#1, 6)3);"
        enewick_graph = enewick_to_digraph(text)
        self.assertEqual(len(enewick_graph.nodes()), 6)

        enewick_phylo = enewick_to_phylonet(text)
        gold_hard = "1,4 1,4,6 1,6 4 6".split()
        hard = cluster_hard(enewick_graph)
        self.assertItemsEqual(hard, gold_hard)
        self.assertEqual(len(enewick_phylo.nodes()), 7)

        clusters = [(1, 2), (2, 3),]
        gold = construct(clusters)
        GM = GraphMatcher(enewick_phylo, gold)
        self.assertTrue(GM.is_isomorphic())

    def test_three(self):
        clusters = ['1,6', '1,4', '1', '4', '1,4,6', '6']
        g = construct(clusters)
        gold = "1 4 6 1,4,6 1,4 1,6 1h".split()
        self.assertEqual(len(g.nodes()), 7)
        self.assertItemsEqual(g.nodes(), gold)

    def test_four(self):
        clusters = ["1,2", "2,3"]
        g = construct(clusters)
        gold = "1 2 3 1,2,3 1,2 2,3 2h".split()
        self.assertEqual(len(g.nodes()), 7)
        self.assertItemsEqual(g.nodes(), gold)

    def test_five(self):
        clusters = ['1,6', '1,4', ]
        g = construct(clusters)
        gold = "1 4 6 1,4,6 1,4 1,6 1h".split()
        self.assertItemsEqual(g.nodes(), gold)

    def test_six(self):
        clusters = [(1, 2), (3, 4), (4, 5), (1, 2, 3), (3, 4, 5), (1, 2, 3, 4)]
        g = construct(clusters)
        gold = ("1 2 3 4 5 1,2,3,4,5 "
                " 3,4h 3h 4h 1,2 1,2,3 1,2,3,4 3,4,5 3,4 4,5").split()
        self.assertItemsEqual(g.nodes(), gold)

    def test_six_b(self):
        clusters = "1,2 3,4 4,5 1,2,3 3,4,5 1,2,3,4".split()
        g = construct(clusters)
        gold = ("1 2 3 4 5 1,2,3,4,5 "
                " 3,4h 3h 4h 1,2 1,2,3 1,2,3,4 3,4,5 3,4 4,5").split()
        self.assertItemsEqual(g.nodes(), gold)
