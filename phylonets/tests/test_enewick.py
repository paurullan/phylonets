#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import unittest

import pyparsing

from networkx.algorithms.isomorphism import GraphMatcher

from enewick import make_enewick_parser
from enewick import MalformedNewickException
from enewick import enewick_to_digraph
from enewick import enewick_to_phylonet

from cluster_networks import construct, calc_hybrid
from cluster_networks import get_leaf_nodes

class TesteNewick(unittest.TestCase):

    def setUp(self):
        self.parser = make_enewick_parser()

    def test_parser_exception(self):
        text = "(1)"
        self.assertRaises(pyparsing.ParseException, self.parser, text)

    def test_malformed_exception(self):
        text = "(1)"
        self.assertRaises(MalformedNewickException, enewick_to_digraph, text)

    def test_one(self):
        text = "(1, 2);"
        enewick_graph = enewick_to_digraph(text)
        clusters = [('1', '2'),]
        gold = construct(clusters)
        GM = GraphMatcher(enewick_graph, gold)
        self.assertTrue(GM.is_isomorphic())

    def test_two(self):
        text = "((1, 2), 3);"
        enewick_graph = enewick_to_digraph(text)
        clusters = [(1, 2), (3,)]
        gold = construct(clusters)
        GM = GraphMatcher(enewick_graph, gold)
        self.assertTrue(GM.is_isomorphic())

    def test_three(self):
        text = "((4, 5#1)2, (#1, 6)3);"
        enewick_graph = enewick_to_digraph(text)
        self.assertEqual(len(enewick_graph.nodes()), 6)
        enewick_graph = calc_hybrid(enewick_graph)
        leafs = get_leaf_nodes(enewick_graph)
        gold_leafs = ['1', '4', '6', ]
        self.assertItemsEqual(leafs, gold_leafs)

        clusters = ["1,2", "2,3"]
        gold = construct(clusters)
        g = enewick_to_phylonet(text)
        GM = GraphMatcher(g, gold)
        self.assertTrue(GM.is_isomorphic())

    def test_four(self):
        text = ("(0,((((((((1,((2,3),4)),(5,6)),(((7,(8,9)),10),"
                "((11,((((12,13),(14,15)),16),17)),((18,19),(20,21))))),"
                "(22,23)),(((24,25),26),((27,28),(29,((30,31),((((32,33),"
                "(34,(35,(36,37)))),(38,(39,((40,41),42)))),43)))))),44),45),46));")
        enewick_graph = enewick_to_digraph(text)
        self.assertEqual(len(enewick_graph.nodes()), 93)
        enewick_phylo = enewick_to_phylonet(text)
        self.assertEqual(len(enewick_phylo.nodes()), 93)

    def test_five(self):
        text = "((1, (2)h#H1)x,(h#H1,3)y)r;"
        clusters = [(1, 2), (2, 3)]
        enewick_graph = enewick_to_digraph(text)
        self.assertEqual(len(enewick_graph.nodes()), 7)
        gold = construct(clusters)
        GM = GraphMatcher(enewick_graph, gold)
        self.assertTrue(GM.is_isomorphic())
