#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import unittest

from hasse import Hasse

class TestHasse(unittest.TestCase):

    def test_empty(self):
        case = [[]]
        gold = []
        self.assertItemsEqual(Hasse(case), gold)

    def test_root(self):
        case = [[1], [2]]
        gold = [
            ((1, 2), (1,)),
            ((1, 2), (2,)),
            ]
        self.assertItemsEqual(Hasse(case), gold)

    def test_one(self):
        case = [[1, 2], [3]]
        gold = [
            ((1, 2), (1,)),
            ((1, 2), (2,)),
            ((1, 2, 3), (1, 2)),
            ((1, 2, 3), (3,)),
            ]
        self.assertItemsEqual(Hasse(case), gold)

    def test_two(self):
        case = [[1], [2, 3], [4]]
                # from → to
        gold = [((1, 2, 3, 4),  (1,)),
                ((2, 3),        (2,)),
                ((2, 3),        (3,)),
                ((1, 2, 3, 4),  (4,)),
                ((1, 2, 3, 4),  (2, 3))]
        self.assertItemsEqual(Hasse(case), gold)

    def test_two_b(self):
        case = [[1, 2], [1, 2, 3], ]
        gold = [ ((1, 2), (1,)),
                 ((1, 2), (2,)),
                 ((1, 2, 3), (3,)),
                 ((1, 2, 3), (1, 2)),
                ]
        self.assertItemsEqual(Hasse(case), gold)

    def test_two_c(self):
        case = [[1, 2], [1, 2, 3], ]
        gold = [ ((1, 2), (1,)),
                 ((1, 2), (2,)),
                 ((1, 2, 3), (3,)),
                 ((1, 2, 3), (3,)),
                 ((1, 2, 3), (1, 2)),
                 ((1, 2, 3), (1, 2)),
                ]
        self.assertNotEqual(Hasse(case), gold)

    def test_three(self):
        case = [[1], [2], [3], [4]]
        gold = [((1, 2, 3, 4), (1,)),
                ((1, 2, 3, 4), (2,)),
                ((1, 2, 3, 4), (3,)),
                ((1, 2, 3, 4), (4,)),
                ]
        self.assertItemsEqual(Hasse(case), gold)

    def test_four(self):
        case = [[1, 2], [3, 4, 5]]
        gold = [((1, 2)   , (1,)),
                ((1, 2)   , (2,)),
                ((3, 4, 5), (3,)),
                ((3, 4, 5), (4,)),
                ((3, 4, 5), (5,)),
                ((1, 2, 3, 4, 5), (1, 2)),
                ((1, 2, 3, 4, 5), (3, 4, 5)),
                ]
        self.assertItemsEqual(Hasse(case), gold)

    def test_five(self):
        case = [[1], [1, 4], [2, 3], [2, 3, 4]]
        gold = [((1, 4), (1,)),
                ((2, 3), (2,)),
                ((2, 3), (3,)),
                ((1, 4), (4,)),
                ((1, 2, 3, 4), (1, 4)),
                ((2, 3, 4), (2, 3)),
                ((2, 3, 4), (4, )),
                ((1, 2, 3, 4), (2, 3, 4)),
                ]
        self.assertItemsEqual(Hasse(case), gold)

    def test_six(self):
        case = [[1, 2], [2, 3], [3, 4], [1, 4]]
        gold = [((1, 2), (1,)),
                ((1, 4), (1,)),
                ((1, 2), (2,)),
                ((2, 3), (2,)),
                ((2, 3), (3,)),
                ((3, 4), (3,)),
                ((3, 4), (4,)),
                ((1, 4), (4,)),
                ((1, 2, 3, 4), (1, 2)),
                ((1, 2, 3, 4), (2, 3)),
                ((1, 2, 3, 4), (3, 4)),
                ((1, 2, 3, 4), (1, 4)),
                ]
        self.assertItemsEqual(Hasse(case), gold)

    def test_seven(self):
        case = [[1, 2], [2, 3], [3, 4], [4, 5]]
        gold = [((1, 2), (1,)),
                ((1, 2), (2,)),
                ((2, 3), (2,)),
                ((2, 3), (3,)),
                ((3, 4), (3,)),
                ((3, 4), (4,)),
                ((4, 5), (4,)),
                ((4, 5), (5,)),
                ((1, 2, 3, 4, 5), (1, 2)),
                ((1, 2, 3, 4, 5), (2, 3)),
                ((1, 2, 3, 4, 5), (3, 4)),
                ((1, 2, 3, 4, 5), (4, 5)),
                ]
        self.assertItemsEqual(Hasse(case), gold)

    def test_eight(self):
        case = [(1, 2, 3), (3, 5), (3, 4, 5), (2, 3), (2, 3, 4, 5)]
        gold = [((1, 2, 3), (1,)),
                ((1, 2, 3), (2, 3)),
                ((1, 2, 3, 4, 5), (1, 2, 3)),
                ((2, 3), (2,)),
                ((2, 3), (3,)),
                ((3, 5), (3,)),
                ((3, 5), (5,)),
                ((3, 4, 5), (4,)),
                ((1, 2, 3, 4, 5), (2, 3, 4, 5)),
                ((2, 3, 4, 5), (2, 3)),
                ((2, 3, 4, 5), (3, 4, 5)),
                ((3, 4, 5), (3, 5)),
                ]
        self.assertItemsEqual(Hasse(case), gold)


    def test_nine(self):
        case = [(1, 2), (3, 5), (3, 4, 5) ]
        # from → to
        gold = [((1, 2), (1,)),
                ((1, 2), (2,)),
                ((3, 5), (3,)),
                ((3, 5), (5,)),
                ((3, 4, 5), (4,)),
                ((1, 2, 3, 4, 5), (1, 2)),
                ((3, 4, 5), (3, 5)),
                ((1, 2, 3, 4, 5), (3, 4, 5))]
        self.assertItemsEqual(Hasse(case), gold)

    def test_ten(self):
        case = [(1, 2), (2, 3), (3, 5), (3, 4, 5) ]
        # from → to
        gold = [((1, 2), (1,)),
                ((1, 2), (2,)),
                ((3, 5), (3,)),
                ((3, 5), (5,)),
                ((2, 3), (2,)),
                ((2, 3), (3,)),
                ((3, 4, 5), (4,)),
                ((3, 4, 5), (3, 5)),
                ((1, 2, 3, 4, 5), (2, 3)),
                ((1, 2, 3, 4, 5), (1, 2)),
                ((1, 2, 3, 4, 5), (3, 4, 5))]
        self.assertItemsEqual(Hasse(case), gold)

class TestHasseText(unittest.TestCase):

    def test_one(self):
        case = ["1,2", "2,3"]
        gold = [
           (('1', '2'), ('1',)),
           (('3', '2'), ('3',)),
           (('1', '2'), ('2',)),
           (('3', '2'), ('2',)),
           (('1', '3', '2'), ('1', '2')),
           (('1', '3', '2'), ('3', '2')),
        ]
        h = Hasse(case)
        self.assertItemsEqual(h, gold)
