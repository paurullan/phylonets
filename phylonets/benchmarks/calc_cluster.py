#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division
from pprint import pprint

from cluster_networks import construct
from cluster_networks import calc_hard_cluster, calc_soft_cluster
from cluster_networks import check_cluster

clusters = [(1, 2)]
clusters = [(1, 2), (3, 4), (4, 5), (1, 2, 3, 4), (3, 4, 5)]

#result = check_cluster(clusters)

G = construct(clusters)
#print(calc_hard_cluster(G))
pprint(calc_soft_cluster(G))

# if result:
#     print("El C_soft == C_hard")
# else:
#     print("No coincideix el C_soft == C_hard")
