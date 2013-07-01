#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

"""
Estudi de les correlacions amb el cost de la generació de treechild
"""

from peewee import SqliteDatabase
from benchmark_classes import BenchmarkCase

# import numpy
# from scipy import stats
import matplotlib.pyplot as plt

TEST_NUMBER = 2

database_filename = "benchmarks.sqlite"
database = SqliteDatabase(database_filename)
database.connect()
B = BenchmarkCase

qs = B.select().where(B.test == TEST_NUMBER).where(B.nodes_conflictius > 0)

conflictius = [q.nodes_conflictius for q in qs]
removibles = [q.arestes_llevables for q in qs]

######
# data = [grau, conflictius, removibles, temps]
data = [conflictius, removibles]
xlabel = u"n nodes conflictius"
ylabel = u"n arestes removibles"
title = u"Correlació entre els nodes conflictius i les removibles"

for x, y in zip(*data):
    plt.plot(x, y, 'ok')

x, y = data

plt.plot((0, 10), (0, 20), 'k--')
plt.plot((0, 20), (0, 20), 'k:')
plt.plot((0, 20), (0, 10), 'k-.')

plt.ylim([1, 21])
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.grid(True)
plt.savefig("conflictius-removibles.pdf")
plt.close()
