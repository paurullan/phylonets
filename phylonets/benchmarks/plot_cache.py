#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

"""
Estudi de les correlacions amb el cost de la generació de treechild
"""
TEST_NUMBER = 1

import string
from peewee import SqliteDatabase
from benchmark_classes import BenchmarkCase

database_filename = "benchmark_cache.sqlite"
db = SqliteDatabase(database_filename)


database_filename = "benchmarks.sqlite"
database = SqliteDatabase(database_filename)
database.connect()

B = BenchmarkCase

qs = B.select().where(B.test == TEST_NUMBER).where(B.temps_soft > 0).order_by(B.subarbres)

ss = "{arbres} \t& {soft:0.4} \t& {cache:0.4} \t& {acc} \\\\"
for letter, q in zip(string.lowercase, qs):
    acc = q.temps_soft / q.temps_soft_cache
    s = ss.format(
        l = letter,
        arbres = q.subarbres,
        soft = q.temps_soft,
        cache = q.temps_soft_cache,
        acc = acc,
    )
    print(s)
# print("\\hline")
from scipy import stats
g = stats.gmean([q.temps_soft_cache for q in qs])
print(" & mitja & geomètrica & {} & \\\\".format(g))
