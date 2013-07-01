#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import numpy
from scipy import stats
import matplotlib.pyplot as plt

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

qs = B.select().where(B.test == TEST_NUMBER).where(B.subarbres < 30*1000)
d = [(q.subarbres, q.temps_soft) for q in qs]

for x, y in d:
    plt.plot(x, y, 'ok')

x, y = zip(*d)
correlation = numpy.corrcoef(x, y)[0][1]
slope, _, _, _, _ = stats.linregress(x, y)

last = max(x)
plt.plot((0, 25000), (0, slope*25000), 'k--')
plt.xlim([0, 22*1000])
plt.ylim([0, 70])
s = u"correlació: {:.4}\n pendent: {:.3}\naprox ops: {}".format(correlation, slope, int(slope**-1))
plt.text(16650, 25, s,
         horizontalalignment='center',
         verticalalignment='center',)
plt.xlabel("Nombre de subarbres")
plt.ylabel("Temps en segons")
plt.title(u"Correlació entre subarbres i temps del soft")
plt.grid(True)
plt.savefig("soft.pdf")
# plt.legend((correlation, slope), ("correlació", "pendent") ) #(rects1[0], rect

plt.close()
