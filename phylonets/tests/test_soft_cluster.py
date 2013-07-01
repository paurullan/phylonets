#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from cluster_networks import cluster_soft
import networkx as nx

from cluster_networks import construct


class TestSoft(unittest.TestCase):

    @classmethod
    def soft(cls, g):
        return cluster_soft(g)

    def test_empty(self):
        G = nx.DiGraph()
        gold = set()
        self.assertItemsEqual(self.soft(G), gold)

    def test_one(self):
        clusters = [(1, 2), ]
        G = construct(clusters)
        gold = "1 2 1,2".split()
        self.assertItemsEqual(self.soft(G), gold)

    def test_two(self):
        clusters = [(1, 2), (3, 4)]
        G = construct(clusters)
        gold = "1 2 3 4 1,2,3,4 1,2 3,4".split()
        self.assertItemsEqual(self.soft(G), gold)

    def test_three(self):
        clusters = [(1, 2), (1, 3)]
        G = construct(clusters)
        gold = "1,2 1,3 1 2 3 1,2,3".split()
        self.assertItemsEqual(self.soft(G), gold)

    def test_three_b(self):
        clusters = [(1, 2), (1, 3), (2, 3)]
        G = construct(clusters)
        gold = "1 2 3 1,2 1,3 2,3 1,2,3".split()
        self.assertItemsEqual(self.soft(G), gold)

    def test_four(self):
        clusters = [(1, 2), (2, 3), (3, 4)]
        G = construct(clusters)
        gold = "1 2 3 4 1,2,3,4 1,2 2,3 3,4".split()
        self.assertItemsEqual(self.soft(G), gold)

    def test_six(self):
        clusters = [(1, 2), (3, 4), (4, 5), (1, 2, 3, 4), (3, 4, 5)]
        G = construct(clusters)
        gold = "1 2 3 4 5 1,2 3,4 4,5 1,2,3 3,4,5 1,2,3,4 1,2,3,4,5".split()
        self.assertItemsEqual(self.soft(G), gold)

class TestSoftLetters(unittest.TestCase):

    def test_one(self):
        clusters = [("human", "rat")]
        G = construct(clusters)
        gold = "human rat human,rat".split()
        self.assertItemsEqual(cluster_soft(G), gold)


class TestSoftComplex(unittest.TestCase):

    @classmethod
    def soft(cls, g):
        return cluster_soft(g)

    def test_complex_1(self):
        edges = [
            ((1, 2, 3, 4, 5), (1, 2, 3, 4)),  # a
            ((1, 2, 3, 4, 5), (3, 4, 5)),  # b
            ((1, 2, 3, 4), (1, )),  # c
            ((1, 2, 3, 4), ('2h', )),  # d
            (('2h', ), (2, 3, 4,)),  # e
            ((2, 3, 4,), (2, )),  # f
            ((2, 3, 4,), ('3h', )),  # g
            ((3, 4, 5), ('3, 4, 5h')),  # h
            ((3, 4, 5), ('3h',)),  # i
            (('3, 4, 5h'), (2, 3, 4, 5)),  # j
            ((2, 3, 4, 5), ('2h', )),  # k
            (('3, 4, 5h'), ('4h',)),  # l
            ((2, 3, 4, 5), (5, )),  # m
            (('3h', ), (3, 4)),  # n
            ((3, 4, ), ('4h', )),  # o
            ((3, 4, ), (3, )),  # p
            (('4h', ), (4, )),  # q
        ]
        G = nx.DiGraph()
        G.add_edges_from(edges)
        gold = ("1 2 3 4 5 1,2,3,4,5 "
                "1,2,3,4 "
                "2,3,5 1,2,3 2,4,5 3,4,5 2,3,4 2,3,4,5 "
                "4,5 2,3 2,5 1,2 3,4 ").split()
        self.assertItemsEqual(self.soft(G), gold)

    def test_complex_2(self):
        clusters = [
            (1, 2), (3, 4), (4, 5), (3, 4, 5), (1, 2, 3, 4)
        ]
        G = construct(clusters)
        gold = ("1 2 3 4 5 1,2,3,4,5 "
                "1,2,3,4 "
                "3,4,5 1,2,3 "
                "4,5 1,2 3,4 ").split()
        self.assertItemsEqual(self.soft(G), gold)

    def test_complex_3(self):
        clusters = [(1, 3), (2, 3), (3, 4), ]
        G = construct(clusters)
        gold = ("1 2 3 4 1,2,3,4 "
                "1,3 2,3 3,4 ").split()
        self.assertItemsEqual(self.soft(G), gold)

    def test_complex_4(self):
        clusters = [(2, 3), (1, 3), (3, 4), (1, 2, 3), (1, 3, 4), ]
        G = construct(clusters)
        gold = [(1,), (2,), (3,), (4,),
                (1, 2), (1, 3), (1, 4), (2, 3), (3, 4),
                (1, 3, 4), (1, 2, 3), (1, 2, 3, 4)]
        gold = ("1 2 3 4 1,2,3,4 "
                "1,2 1,3 1,4 2,3 3,4 1,3,4 1,2,3 ").split()
        self.assertItemsEqual(self.soft(G), gold)

    def test_complex_5(self):
        clusters = [(1, 2), (3, 4), (4, 5), (1, 2, 3, 4), (3, 4, 5), ]
        G = construct(clusters)
        gold = [(1,), (2,), (3,), (4,), (5, ),
                (1, 2), (3, 4), (4, 5),
                (1, 2, 3), (3, 4, 5),
                (1, 2, 3, 4),
                (1, 2, 3, 4, 5)]
        gold = ("1 2 3 4 5 1,2,3,4,5 "
                "1,2,3,4 "
                "1,2 3,4 4,5 1,2,3 3,4,5 ").split()
        self.assertItemsEqual(self.soft(G), gold)

    def test_complex_6(self):
        """ 8 nodes emparellats, 8 híbrids, 196 crides, .25 segons"""
        clusters = [
            (1, 2), (2, 3), (3, 4), (4, 5),
            (5, 6), (6, 7), (7, 8), (8, 1), ]
        G = construct(clusters)
        gold = ("1 2 3 4 5 6 7 8 1,2,3,4,5,6,7,8 "
                "7,8 5,6 2,3 1,2 6,7 1,8 4,5 3,4 ").split()
        self.assertItemsEqual(self.soft(G), gold)
