#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import time

import sys
import cPickle as pickle
from multiprocessing import Pool

import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from cluster_networks import construct, hybrid_nodes
from cluster_networks import get_leaf_nodes
from cluster_networks import cluster_soft, construct_treechild
from cluster_networks import potential_number_of_calls
from cluster_networks import hybridization_degree, removable_edges
from cluster_networks import is_treechild, problematic_treechild_nodes

from benchmark_classes import BenchmarkCase

TEST_NUMBER = 1
MAX_SUBARBRES = 30*1000 * 4
SOFT_TIMES = 100

from redis_cache import cache_it, SimpleCache


def test_cluster(cluster):
    g = construct(cluster)
    test_case(g)

def test_case(g):
    test = TEST_NUMBER
    nodes = len(g.nodes())
    fulles = len(get_leaf_nodes(g))
    arestes = len(g.edges())
    hibrids = len(hybrid_nodes(g))
    grau_hibriditzacio = hybridization_degree(g)
    arestes_llevables = len(removable_edges(g))
    es_treechild = is_treechild(g)
    nodes_conflictius = len(problematic_treechild_nodes(g))
    subarbres = potential_number_of_calls(g)
    # soft
    if subarbres < MAX_SUBARBRES:
        begin_soft = time.time()
        cluster_soft_cache(g)
        end_soft = time.time()
        temps_soft = end_soft - begin_soft
        begin_soft_cache = time.time()
        for i in range(SOFT_TIMES):
            cluster_soft_cache(g)
        end_soft_cache = time.time()
        temps_soft_cache = (end_soft_cache - begin_soft_cache) / SOFT_TIMES
    else:
        temps_soft, temps_soft_cache = -1, -1
    # tree-child
    if not es_treechild:
        begin_families = time.time()
        families = construct_treechild(g)
        end_families = time.time()
        n_families = len(families)
        temps_families = end_families - begin_families
    else:
        n_families, temps_families = 0, 0
    BenchmarkCase.create(
        test = test,
        fulles = fulles,
        nodes = nodes,
        arestes = arestes,
        hibrids = hibrids,
        subarbres = subarbres,
        grau_hibriditzacio = grau_hibriditzacio,
        temps_soft = temps_soft,
        temps_soft_cache = temps_soft_cache,
        arestes_llevables = arestes_llevables,
        es_treechild = es_treechild,
        nodes_conflictius = nodes_conflictius,
        temps_families = temps_families,
        n_families = n_families,
    )

class MultiSessionCache(SimpleCache):
    key_str = "multisession-cache"

    def make_key(self, key):
        return MultiSessionCache.key_str + "-" + str(key)

    def get_set_name(self):
        return MultiSessionCache.key_str

my_cache = MultiSessionCache(hashkeys=True)
@cache_it(cache=my_cache)
def cluster_soft_cache(g):
    return cluster_soft(g)

if __name__ == '__main__':
    filename = "stress.pickle"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    with open(filename) as f:
        cases = pickle.load(f)
    BenchmarkCase.create_table(fail_silently=True)
    pool = Pool()
    pool.map(test_cluster, cases)
