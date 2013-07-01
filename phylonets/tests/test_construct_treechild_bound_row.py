#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import unittest

import logging
log = logging.getLogger(__name__)

import networkx as nx

from cluster_networks import construct
from cluster_networks import check_problematic_row

class TestRowProblematic(unittest.TestCase):

    def test_empty_graph(self):
        g = nx.DiGraph()
        self.assertFalse(check_problematic_row(g))

    def test_one(self):
        clusters = [(1,2), (2,3), (1,3)]
        g = construct(clusters)
        self.assertTrue(check_problematic_row(g))

    def test_neg_one(self):
        clusters = [(1,2), (2,3), (3,4)]
        g = construct(clusters)
        self.assertFalse(check_problematic_row(g))

    def test_neg_two(self):
        clusters = [(1,2), (3,4)]
        g = construct(clusters)
        self.assertFalse(check_problematic_row(g))

    def test_neg_three(self):
        clusters = [(1,2), (2, 3), (3,4), (4,5)]
        g = construct(clusters)
        self.assertFalse(check_problematic_row(g))

    def test_neg_four(self):
        clusters = [(1,2), (2, 3), (3,4), (4,5), (5,6)]
        g = construct(clusters)
        self.assertFalse(check_problematic_row(g))
