#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module exists because in version 0.3.7 of rq you cannot delay functions
from the __main__ and I prefer not to put the cache into the main
cluster_networks module.
"""

from redis_cache import cache_it

from phylonets.cluster_networks import cluster_soft as calc_soft_cluster
from phylonets.cluster_networks import cluster_hard as calc_hard_cluster
from phylonets.cluster_networks import construct_treechild

@cache_it()
def cluster_soft(network):
    return calc_soft_cluster(network)

@cache_it()
def cluster_hard(network):
    return calc_hard_cluster(network)


@cache_it()
def tree_child_families(network):
    return construct_treechild(network)
