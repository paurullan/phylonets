#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import sys
import cPickle as pickle

import logging
log = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)

from itertools import combinations
from random import choice

def create_case(N):
    initial = range(1, N + 1)
    result = []
    combs_4 = list(combinations(initial, 4))
    combs_2 = list(combinations(initial, 2))
    for i in range(N // 4):
        result.append(choice(combs_4))
    for i in range(N // 5):
        result.append(choice(combs_2))
    return result

cases = []
for i in range(10, 61, 5):
    log.debug(i)
    for j in range(5):
        log.debug(j)
        cases.append(create_case(i))

filename = "stress.pickle"
if len(sys.argv) > 1:
    filename = sys.argv[1]
with open(filename, 'w') as f:
    pickle.dump(cases, f)

# from pprint import pprint
# pprint(cases)
