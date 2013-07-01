#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import logging
log = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)

from peewee import SqliteDatabase
from benchmark_classes import BenchmarkCase

TIMEOUT = 70
TEST_NUMBER = 1

database_filename = "benchmarks.sqlite"
database = SqliteDatabase(database_filename)
database.connect()
B = BenchmarkCase

qs = B.select().where(B.test == TEST_NUMBER)

xarxes = qs.count()
treechilds = qs.where(B.es_treechild).count()
generades = qs.where(B.n_families > 0).count()
soft = qs.where(B.temps_soft < 0).count()

qs = qs.order_by(B.subarbres)
s = ("{fulles} & {arbres} & {hibrids} & {grau} & {subarbres} & {soft} & "
     # "{llevables} & {t_families} & {n_families} \\\\")
     "{llevables} & {t_families} \\\\")
print(s)
for q in qs:
    if q.temps_soft < 0:
        soft = "Time out"
    else:
        soft = "{0:.4}".format(q.temps_soft)
    if q.temps_families < 0:
        families = "TO"
    else:
        families = "{0:.4}".format(q.temps_families)
    vals = {
        'fulles': q.fulles,
        'arbres': q.nodes - q.fulles - q.hibrids,
        'hibrids': q.hibrids,
        'grau': q.grau_hibriditzacio,
        'subarbres': q.subarbres,
        'soft': soft,
        'conflictius': q.nodes_conflictius,
        'llevables': q.arestes_llevables,
        't_families': families,
        'n_families': q.n_families,
    }
    print(s.format(**vals))
