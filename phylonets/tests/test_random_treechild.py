#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import unittest

from cluster_networks import construct
from cluster_networks import construct_treechild

class TestTreeChildFromRandom(unittest.TestCase):

    def test_random_1(self):
        clusters = [(1, 5, 7, 10), (2, 4, 8, 10), (1, 3), (3, 4)]
        gold = 0
        result = construct_treechild(construct(clusters))
        self.assertEqual(len(result), gold)
