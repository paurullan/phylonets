#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import time

import sys
import cPickle as pickle

import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

from cluster_networks import construct
from cluster_networks import cluster_soft
from cluster_networks import potential_number_of_calls

from redis_cache import cache_it, SimpleCache

from peewee import Model, SqliteDatabase
from peewee import IntegerField, FloatField

from timeit import Timer

from multiprocessing import Pool

database_filename = "benchmark_cache.sqlite"
db = SqliteDatabase(database_filename)

class BenchmarkCacheCase(Model):
    subarbres = IntegerField()
    soft = FloatField()
    cache = FloatField()

    class Meta:
        database = db


def test_case(g):
    subarbres = potential_number_of_calls(g)
    # càlcul soft
    # begin_soft = time.time()
    # cluster_soft_cache(g)
    # end_soft = time.time()
    # temps_soft = end_soft - begin_soft
    # re-soft amb cache

    # cluster_soft_cache(g)
    f = lambda: cluster_soft_cache(g)
    T = Timer(f)
    repeat, number = 5, 1000
    vals = T.repeat(repeat=repeat, number=number)
    temps_cache = min(vals) / number
    log.info(temps_cache)
    return
    BenchmarkCacheCase.create(
        subarbres=subarbres,
        soft=temps_soft,
        cache=temps_cache,
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
    cluster_soft(g)

def test_cluster(cluster):
    g = construct(cluster)
    test_case(g)

if __name__ == '__main__':
    filename = "stress.pickle"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    with open(filename) as f:
        cases = pickle.load(f)
    cases = cases[:15]
    # cases = cases[25:35]
    BenchmarkCacheCase.create_table(fail_silently=True)
    pool = Pool()
    pool.map(test_cluster, cases)
