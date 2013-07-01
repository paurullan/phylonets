#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

"""
Estudi de les correlacions amb el cost de la generació de treechild
"""

from peewee import SqliteDatabase
from benchmark_classes import BenchmarkCase

import numpy
from scipy import stats
import matplotlib.pyplot as plt

TEST_NUMBER = 1

database_filename = "benchmarks.sqlite"
database = SqliteDatabase(database_filename)
database.connect()
B = BenchmarkCase

qs = B.select().where(B.test == TEST_NUMBER)

grau = [q.nodes for q in qs]
conflictius = [q.nodes_conflictius for q in qs]
llevables = [q.arestes_llevables for q in qs]
temps = [q.temps_families for q in qs]

# # # pel temps logarítmic
temps_log = [t if t else 0.001 for t in temps]
temps_log = map(numpy.log10, temps_log)

######
# data = [grau, conflictius, llevables, temps]
data = [grau, temps]
xlabel = u"Grau d'hibridització"
title = u"Correlació entre el grau d'hibridització i t. per tree-child"

for x, y in zip(*data):
    plt.plot(x, y, 'ok')

plt.xlabel(xlabel)
plt.title(title)
plt.grid(True)
plt.ylabel(u"Temps en segons")
plt.savefig("hibriditzacio.pdf")
plt.close()

# log
x, y = [grau, temps_log]
correlation = numpy.corrcoef(x, y)[0][1]
slope, _, _, _, _ = stats.linregress(x, y)
plt.plot((min(x), max(x)), (min(y), slope*max(y)), 'k--')
for x, y in zip(*data):
    plt.plot(x, y, 'ok')

xlabel = u"Grau d'hibridització; c: {}; p: {} ".format(correlation, slope)
plt.xlabel(xlabel)
plt.title(title)
plt.grid(True)
plt.ylabel(u"Temps en log10 segons")
plt.savefig("hibriditzacio-log.pdf")
plt.close()

######
# data = [grau, conflictius, llevables, temps]
data = [conflictius, temps]
xlabel = u"Nombre de nodes no tree-child (conflictius)"
title = u"Correlació entre els nodes conflictius i t. per tree-child"

for x, y in zip(*data):
    plt.plot(x, y, 'ok')

plt.xlabel(xlabel)
plt.title(title)
plt.grid(True)
plt.ylabel(u"Temps en segons")
plt.savefig("conflictius.pdf")
plt.close()

# log
x, y = [grau, temps_log]
correlation = numpy.corrcoef(x, y)[0][1]
slope, _, _, _, _ = stats.linregress(x, y)
plt.plot((min(x), max(x)), (min(y), slope*max(y)), 'k--')
for x, y in zip(*data):
    plt.plot(x, y, 'ok')
xlabel = u"Grau n conflictius; c: {}; p: {} ".format(correlation, slope)
plt.xlabel(xlabel)
plt.title(title)
plt.grid(True)
plt.ylabel(u"Temps en log10 segons")
plt.savefig("conflictius-log.pdf")
plt.close()

######
# data = [grau, conflictius, llevables, temps]
data = [llevables, temps]
xlabel = u"Nombre d'arestes llevables"
title = u"Correlació entre el nombre d'arestes llevables i t. per tree-child"

for x, y in zip(*data):
    plt.plot(x, y, 'ok')

x, y = data
correlation = numpy.corrcoef(x, y)[0][1]
slope, _, _, _, _ = stats.linregress(x, y)

plt.xlabel(xlabel)
plt.title(title)
plt.grid(True)
plt.ylabel(u"Temps en segons")
plt.savefig("llevables.pdf")
plt.close()

# log
x, y = [llevables, temps_log]
correlation = numpy.corrcoef(x, y)[0][1]
slope, _, _, _, _ = stats.linregress(x, y)
plt.plot((min(x), max(x)), (min(y), slope*max(y)), 'k--')
for x, y in zip(*data):
    plt.plot(x, y, 'ok')

xlabel = u"#arestes removibles; c: {}; p: {} ".format(correlation, slope)
plt.xlabel(xlabel)
plt.title(title)
plt.grid(True)
plt.ylabel(u"Temps en log10 segons")
plt.savefig("llevables-log.pdf")
plt.close()

"""
0.936463956372
0.077595620199
-----
0.932377330818
0.614557005513
-----
0.947762427664
0.17308497087
"""
