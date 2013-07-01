#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import logging
log = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)

from peewee import Model, SqliteDatabase
from peewee import IntegerField, FloatField, BooleanField

database_filename = "benchmarks.sqlite"
db = SqliteDatabase(database_filename)

class BenchmarkCase(Model):
    test = IntegerField()
    nodes = IntegerField()
    fulles = IntegerField()
    arestes = IntegerField()
    hibrids = IntegerField()
    grau_hibriditzacio = IntegerField()
    subarbres = IntegerField()
    temps_soft = FloatField()
    temps_soft_cache = FloatField()
    arestes_llevables = IntegerField()
    es_treechild = BooleanField()
    nodes_conflictius = IntegerField()
    temps_families = FloatField()
    n_families = IntegerField()

    class Meta:
        database = db
