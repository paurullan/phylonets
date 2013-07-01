#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

# [ [1, 2, 3], [4] ]
def Hasse(clusters):
    # corner case for the empty input
    if not clusters:
        return []
    if len(clusters) == 1 and not clusters[0]:
        return []

    cluster_dict, level_max = _construct_hasse(clusters)
    results = []
    for levels in range(1, level_max):
        for cluster in cluster_dict[levels]:
            for cl_level in range(levels+1, level_max+1):
                [check_in(cluster, x, results) for x in cluster_dict[cl_level]]
    return results


def _construct_hasse(clusters):
    max_set = set()
    for s in clusters:
        if isinstance(s, str):
            elems = s.split(",")
        else:
            elems = s
        for elem in elems:
            max_set.add(elem)
    level_max = len(max_set)

    # cluster_dict has the tree cluster structure
    cluster_dict = {x: [] for x in range(1, level_max+1)}
    for cluster in clusters:
        if isinstance(cluster, str):
            s = cluster.split(",")
            cluster_lvl = len(s)
            cluster_dict[cluster_lvl].append(s)
        else:
            cluster_lvl = len(cluster)
            cluster_dict[cluster_lvl].append(cluster)

    # init for single elements pex: [ [1], [2], [3], ]
    cluster_dict[1] = []
    for item in list(max_set):
        cluster_dict[1].append([item])

    if not list(max_set) in cluster_dict[level_max]:
        cluster_dict[level_max].append(list(max_set))

    return cluster_dict, level_max


def check_in(a, b, results):
    a, b = set(a), set(b)
    if not a.issubset(b):
        return
    for orig, dest in results:
        orig, dest = set(orig), set(dest)
        if orig.issubset(b) and a == dest:
            return
    results.append((tuple(b), tuple(a)))
