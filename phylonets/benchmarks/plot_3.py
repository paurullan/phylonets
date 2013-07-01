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

#TEST_NUMBER = 36
TEST_NUMBER = 39

database_filename = "benchmarks.sqlite"
database = SqliteDatabase(database_filename)
database.connect()
B = BenchmarkCase

# qs = B.select().where(B.test == TEST_NUMBER).where(B.temps_families > 0)

# tallam als 70 segons
qs = B.select().where(B.test == TEST_NUMBER).where(0 < B.temps_families < 70).where(B.arestes_llevables > 0)

grau = [q.nodes for q in qs]
conflictius = [q.nodes_conflictius for q in qs]
llevables = [q.arestes_llevables for q in qs]
temps = [q.temps_families for q in qs]

### pel temps logarítmic
temps_log = [t if t else 0.001 for t in temps]
temps_log = map(numpy.log10, temps_log)

######
# data = [grau, conflictius, llevables, temps]
data = [grau, temps]
xlabel = u"Grau d'hibridització"
title = u"Correlació entre el grau d'hibridització i t. per tree-child"

for x, y in zip(*data):
    plt.plot(x, y, 'o')

x, y = data
correlation = numpy.corrcoef(x, y)[0][1]
slope, _, _, _, _ = stats.linregress(x, y)

plt.xlabel(xlabel)
plt.title(title)
plt.grid(True)
plt.ylabel(u"Temps en segons")
plt.savefig("hibriditzacio.pdf")
plt.close()
#
# y = temps_log
# correlation = numpy.corrcoef(x, y)[0][1]
# slope, _, _, _, _ = stats.linregress(x, y)

# plt.plot((min(x), max(x)), (min(y), slope*max(y)), 'k--')
# plt.plot((min(x), max(x)), (min(y)+.5, slope*max(y)+.5), 'k--')

# plt.xlabel(xlabel)
# plt.title(title)
# plt.grid(True)
# plt.ylabel(u"Temps en log10 segons")
# plt.savefig("hibriditzacio-log.pdf")
# plt.savefig("hibriditzacio.pdf")
# plt.close()

######
# data = [grau, conflictius, llevables, temps]
data = [conflictius, temps]
xlabel = u"Nombre de nodes no tree-child (conflictius)"
title = u"Correlació entre els nodes conflictius i t. per tree-child"

for x, y in zip(*data):
    plt.plot(x, y, 'o')

x, y = data
correlation = numpy.corrcoef(x, y)[0][1]
slope, _, _, _, _ = stats.linregress(x, y)

# plt.plot((min(x), max(x)), (min(y), slope*max(y)), 'k--')
# plt.plot((min(x), max(x)), (min(y)+.5, slope*max(y)+.5), 'k--')

plt.xlabel(xlabel)
plt.title(title)
plt.grid(True)
# plt.ylabel(u"Temps en log10 segons")
# plt.savefig("conflictius-log.pdf")
plt.xlim([0, 8])
plt.ylabel(u"Temps en segons")
plt.savefig("conflictius.pdf")
plt.close()

######
# data = [grau, conflictius, llevables, temps]
data = [llevables, temps]
xlabel = u"Nombre d'arestes removibles"
title = u"Correlació entre el nombre d'arestes removibles i t. per tree-child"

for x, y in zip(*data):
    plt.plot(x, y, 'o')

x, y = data
correlation = numpy.corrcoef(x, y)[0][1]
slope, _, _, _, _ = stats.linregress(x, y)

# plt.plot((min(x), max(x)), (min(y), slope*max(y)), 'k--')
# plt.plot((min(x), max(x)), (min(y)+.5, slope*max(y)+.5), 'k--')

plt.xlabel(xlabel)
plt.title(title)
plt.grid(True)
plt.xlim([1, 15])
plt.ylabel(u"Temps en segons")
plt.savefig("llevables.pdf")
#plt.ylabel(u"Temps en log10 segons")
#plt.savefig("llevables-log.pdf")
plt.close()


print(qs.count())
