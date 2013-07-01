#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import unittest

from cluster_networks import construct
from cluster_networks import cluster_soft
from cluster_networks import remove_edge

class TestClusterFromRandom(unittest.TestCase):

    def test_random_0(self):
        clusters = [(3, 8), (2, 6), (3, 4), (1, 7),
                    (2, 3, 5, 7), (1, 4, 7, 8),
                    (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,)]
        gold = ("1 2 3 4 5 6 7 8 1,2,3,4,5,6,7,8 "
                "1,4,7,8 2,3,5,7 2,6 3,8 1,7 3,4 1,4 1,8 2,5 3,5 5,7 "
                "1,4,7 1,4,8 1,7,8 2,3,5 2,5,7 3,5,7 ").split()
        result = cluster_soft(construct(clusters))
        self.assertItemsEqual(result, gold)

    def test_random_2(self):
        clusters = [
            (3, 5), (2, 5), (5, 9), (4, 10), (1, 2),
            (3, 4, 6, 7, 8), (2, 5, 8, 9, 10),
            (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,)]
        gold = ("1 2 3 4 5 6 7 8 9 10 1,10,2,3,4,5,6,7,8,9 "
                "5,9 10,2,5,8,9 2,5,8,9 8,9 2,5,9 2,5 10,2,8,9 1,2 6,7 "
                "10,5,8,9 4,6,7,8 2,8,9 3,6,7 10,4 10,5,9 6,7,8 10,9 2,9 "
                "10,2,5,9 3,5 10,8,9 5,8,9 10,2,9  3,6,7,8 3,4,6,7 4,6,7 3,4,6,7,8 "
                "").split()
        result = cluster_soft(construct(clusters))
        self.assertItemsEqual(result, gold)
