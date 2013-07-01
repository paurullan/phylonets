#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import logging
log = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)

from peewee import SqliteDatabase
from benchmark_classes import BenchmarkCase

TEST_NUMBER = 2

database_filename = "benchmarks.sqlite"
database = SqliteDatabase(database_filename)
database.connect()
B = BenchmarkCase

qs = B.select().where(B.test == TEST_NUMBER).order_by(B.arestes_llevables, B.subarbres)

qs = qs.order_by(B.subarbres)
s = ("{fulles} & {arbres} & {hibrids} & {grau} & \t {subarbres} \t & "
     "{conflictius} & {llevables} & \t {t_families} \t& \t {n_families} \\\\")
print(s)
for q in qs:
    if q.temps_families < 0:
        families = "Time out"
        n_families = "-"
    else:
        families = "{}".format(q.temps_families)
        n_families = q.n_families
    vals = {
        'fulles': q.fulles,
        'arbres': q.nodes - q.fulles - q.hibrids,
        'hibrids': q.hibrids,
        'grau': q.grau_hibriditzacio,
        'subarbres': q.subarbres,
        'conflictius': q.nodes_conflictius,
        'llevables': q.arestes_llevables,
        't_families': families,
        'n_families': n_families,
    }
    print(s.format(**vals))

print("amb timeout")
print(qs.where(B.temps_families < 0).count()  )
