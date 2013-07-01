#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import unittest

# from networkx.algorithms.isomorphism import GraphMatcher

from cluster_networks import construct_treechild
from cluster_networks import is_treechild
# from cluster_networks import cluster_hard

# from enewick import enewick_to_digraph
from enewick import enewick_to_phylonet


class TestDataSet(unittest.TestCase):

    # def test_one(self):
    #     text = "(CIOIN,((HUMAN,MACMU),(MACMU,(MACMU,((MACMU,(MACMU,MACMU)),(HUMAN,(MACMU,((((((HUMAN,MACMU),((MACMU,MACMU),(((MACMU,(MACMU,(MACMU,MACMU))),MACMU),HUMAN))),((MACMU,((HUMAN,PANTR),MACMU)),(MACMU,(MACMU,MACMU)))),(MACMU,MACMU)),(MACMU,MACMU)),(HUMAN,(MACMU,(HUMAN,((((MACMU,(MACMU,(MACMU,(HUMAN,PANTR)))),MACMU),((MACMU,(HUMAN,MACMU)),MACMU)),(((MACMU,MACMU),(HUMAN,PANTR)),((((((MACMU,(HUMAN,MACMU)),((PANTR,HUMAN),MACMU)),(CIOIN,(PANTR,HUMAN))),(MACMU,((((MACMU,HUMAN),(MACMU,(MACMU,((PANTR,HUMAN),((MACMU,MACMU),HUMAN))))),(MACMU,MACMU)),((MACMU,((((((HUMAN,MACMU),((((MACMU,MACMU),MACMU),(MACMU,MACMU)),MACMU)),(PANTR,HUMAN)),MACMU),MACMU),MACMU)),(CIOIN,(MACMU,HUMAN)))))),((((MACMU,(MACMU,MACMU)),(MACMU,PANTR)),(HUMAN,MACMU)),(MACMU,MACMU))),(((MACMU,(PANTR,HUMAN)),(((HUMAN,MACMU),((CIOIN,CIOIN),(((HUMAN,HUMAN),PANTR),(HUMAN,(HUMAN,PANTR))))),HUMAN)),(((PANTR,HUMAN),MACMU),((HUMAN,PANTR),(MACMU,HUMAN))))))))))))))))));"
    #     enewick_graph = enewick_to_phylonet(text)
    #     self.assertEqual(len(enewick_graph.nodes()), 123)
    #     self.assertTrue(is_treechild(enewick_graph))
    #     tc = construct_treechild(enewick_graph)
    #     self.assertFalse(tc)

    pass
