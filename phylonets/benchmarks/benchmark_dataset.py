#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

from enewick import enewick_to_phylonet

import time
import itertools

import logging
log = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)

from multiprocessing import Pool

from cluster_networks import cluster_hard, construct
from cluster_networks import hybrid_nodes
from cluster_networks import construct_treechild
from cluster_networks import potential_number_of_calls
from cluster_networks import hybridization_degree, removable_edges
from cluster_networks import is_treechild, problematic_treechild_nodes
from cluster_networks import get_leaf_nodes

from benchmark_classes import BenchmarkCase

TEST_NUMBER = 2

MAX_ARESTES = 10
SOFT_TIMES = 100

def benchmark_nets(g):
    # atributs varis
    arestes_llevables = len(removable_edges(g))
    fulles = len(get_leaf_nodes(g))
    nodes = len(g.nodes())
    arestes = len(g.edges())
    hibrids = len(hybrid_nodes(g))
    grau_hibriditzacio = hybridization_degree(g)
    es_treechild = is_treechild(g)
    nodes_conflictius = len(problematic_treechild_nodes(g))
    subarbres = potential_number_of_calls(g)
    temps_soft, temps_soft_cache = -1, -1
    n_families, temps_families = -1, -1
    # tree-child
    if not es_treechild:
        if arestes_llevables < MAX_ARESTES:
            begin_families = time.time()
            families = construct_treechild(g)
            end_families = time.time()
            temps_families = end_families - begin_families
            n_families = len(families)
    else:
        n_families, temps_families = 0, 0
    BenchmarkCase.create(
        test = TEST_NUMBER,
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

def construct_network(comb):
    left, right = comb
    h_left = cluster_hard(left)
    h_right = cluster_hard(right)
    clusters = {cl for cl in itertools.chain(h_left, h_right)}
    g = construct(clusters)
    return g

filename = "datasets/grassData/all"
with open(filename) as f:
    cases = [line.strip() for line in f.readlines()]

BenchmarkCase.create_table(fail_silently=True)
pool = Pool()
phylotrees = pool.map(enewick_to_phylonet, cases)
combs = itertools.combinations(phylotrees, 2)
nets = (construct_network(n) for n in combs)
pool.imap_unordered(benchmark_nets, nets)
pool.close()
pool.join()
