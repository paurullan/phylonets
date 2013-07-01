#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

from peewee import SqliteDatabase
from benchmark_classes import BenchmarkCase

# TEST_NUMBER = 36
TEST_NUMBER = 39

database_filename = "benchmarks.sqlite"
database = SqliteDatabase(database_filename)
database.connect()
B = BenchmarkCase

qs = B.select().where(B.test == TEST_NUMBER)

# nodes & arestes & grau & subarbres & confl. & llevables & t.generar (s) & generats \\
s = "{nodes} & {arestes} & {grau} & {subarbres:,} & {conflictius} & {llevables} & {t_families:.3} & {n_families} \\\\"

qs = qs.order_by(B.arestes_llevables, B.temps_families)

for q in qs:
    ss = s.format(
        nodes=q.nodes,
        arestes=q.arestes,
        grau=q.grau_hibriditzacio,
        subarbres=q.subarbres,
        conflictius=q.nodes_conflictius,
        llevables=q.arestes_llevables,
        t_families=q.temps_families,
        n_families=q.n_families,
        )
    print(ss)
