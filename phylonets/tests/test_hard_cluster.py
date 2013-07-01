#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import unittest

import networkx as nx

from cluster_networks import construct
from cluster_networks import cluster_hard


class TestHardCluster(unittest.TestCase):

    def test_empty(self):
        G = nx.DiGraph()
        gold = set()
        self.assertItemsEqual(cluster_hard(G), gold)

    def test_one(self):
        clusters = [(1, 2)]
        G = construct(clusters)
        gold = "1 2 1,2".split()
        self.assertItemsEqual(cluster_hard(G), gold)

    def test_three(self):
        clusters = [(1, 2), (3, 4)]
        G = construct(clusters)
        gold = "1 2 3 4  1,2,3,4  1,2 3,4".split()
        self.assertItemsEqual(cluster_hard(G), gold)

    def test_four(self):
        clusters = [(1, 2, 3)]
        G = construct(clusters)
        gold = "1 2 3 1,2,3".split()
        self.assertItemsEqual(cluster_hard(G), gold)

    def test_five(self):
        edges = [
            ((1, 2, 3, 4), (4, )),
            ((4, ), (3, )),
            ((1, 2,), (1, )),
            ((1, 2,), (2, )),
            ((1, 2, 3, 4), (1, 2, )),
            ]
        G = nx.DiGraph()
        G.add_edges_from(edges)
        gold = "1 2 3 1,2 1,2,3".split()
        self.assertItemsEqual(cluster_hard(G), gold)

    def test_six(self):
        edges = [
            ((1, 2, 3, 4), (1, 2)),
            ((1, 2, 3, 4), (3, 4)),
            ((3, 4, ), (3, )),
            ((3, 4, ), (4, )),
            ((1, 2,), (1, )),
            ((1, 2,), (2, )),
        ]
        G = nx.DiGraph()
        G.add_edges_from(edges)
        gold = "1 2 3 4 1,2 3,4 1,2,3,4".split()
        self.assertItemsEqual(cluster_hard(G), gold)

    def test_seven(self):
        edges = [("['1', u'4', u'6']", u'3'),
                 ("['1', u'4', u'6']", u'2'),
                 ('1h', '1'),
                 (u'3', '1h'),
                 (u'3', u'6'),
                 (u'2', '1h'),
                 (u'2', u'4') ]
        G = nx.DiGraph()
        G.add_edges_from(edges)
        gold = ['1', '4', '6', '1,4,6', '1,4', '1,6', ]
        self.assertItemsEqual(cluster_hard(G), gold)
