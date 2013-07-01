#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

"""
Estudi de les correlacions amb el cost de la generació de treechild
"""

from peewee import SqliteDatabase
from benchmark_classes import BenchmarkCase

import matplotlib.pyplot as plt

TEST_NUMBER = 2

database_filename = "benchmarks.sqlite"
database = SqliteDatabase(database_filename)
database.connect()
B = BenchmarkCase

qs = B.select().where(B.test == TEST_NUMBER).where(B.arestes_llevables > 0)
llevables = [q.arestes_llevables for q in qs]
temps = [q.temps_families for q in qs]

######
# data = [grau, conflictius, llevables, temps]
data = [llevables, temps]
plt.xlim([0, 21])
plt.ylim([-1, 950])
xlabel = u"Nombre d'arestes removibles"
title = u"Correlació entre el nombre d'arestes removibles i t. per tree-child"

for x, y in zip(*data):
    if 0 < y < 800:
        plt.plot(x, y, '.k')
    else:
        plt.plot(x, 900, 'xk')


plt.xlabel(xlabel)
plt.title(title)
plt.grid(True)
plt.ylabel(u"Temps en segons")
plt.savefig("llevables.pdf")
plt.close()
