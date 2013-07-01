#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

__version__ = "0.0.1"

import re
import sys
import json
import ast
import urllib
import time

from bottle import route, run, static_file
from bottle import redirect, view, post, request
from bottle import Response

import networkx as nx

from redis import Redis
from rq import Queue

import logging
log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

from phylonets import cluster_networks
from phylonets import enewick

# importing the cached calculations
from proxy import cluster_soft, cluster_hard, tree_child_families

DEBUG = False
MAX_SUBTREES = 25*1000
MAX_LABEL = 12
MAX_QUOTED = 4400

index_examples = [
    # name, clusters
    ('Remove edge, 2 tree-child',
     urllib.quote_plus("(1, 2), (3, 4), (4, 5), (1, 2, 3), (3, 4, 5), (1, 2, 3, 4)"),),
    ('Remove edge, 1 tree-child',
     urllib.quote_plus("(1, 2), (2, 3), (3, 4), (3, 4, 5), (1, 2, 3), (1, 2, 3, 4)"),),
    ('Remove edge, non tree-child',
     urllib.quote_plus("(1, 2), (2, 3, 4), (4, 5), (2, 4), (1, 2, 3, 4)"),),
     ('Little phylo tree',
     #"(((((HUMAN,PANTR),MACMU),CANFA),(MOUSE,RAT)),CHICK);"
     urllib.quote_plus("'CANFA,CHICK,HUMAN,MACMU,MOUSE,PANTR,RAT', 'HUMAN,MACMU,PANTR', 'HUMAN,PANTR', 'CANFA', 'MACMU', 'CANFA,HUMAN,MACMU,MOUSE,PANTR,RAT', 'CHICK', 'PANTR', 'MOUSE,RAT', 'RAT', 'CANFA,HUMAN,MACMU,PANTR', 'HUMAN', 'MOUSE'"), ),
]

def get_dot(G_orig):
    """Change labels and colors to be presented with graphviz"""
    G = G_orig.copy()
    cluster_networks.relabel_graph(G)
    tr = {}
    for node in G.nodes_iter():
        tr[node] = '"{}"'.format(node)
    nx.relabel_nodes(G, tr, copy=False)
    for node in G.nodes_iter():
        label = str(node)
        if len(label) > MAX_LABEL:
            label = u'{}..."'.format(label[:MAX_LABEL])
        G.node[node]['label'] = label
    for node in cluster_networks.get_leaf_nodes(G):
        G.node[node]['color'] = "blue"
    for node in cluster_networks.hybrid_nodes(G):
        G.node[node]['color'] = "#7BFF74"  # light green
        G.node[node]['style'] = 'filled'
    for node in cluster_networks.get_root_nodes(G):
        G.node[node]['color'] = "orange"
    for node in cluster_networks.problematic_treechild_nodes(G):
        G.node[node]['color'] = "#FF77EB"  # light pink
        G.node[node]['style'] = 'filled'
    for u, v in cluster_networks.removable_edges(G):
        G.edge[u][v]['color'] = "red"
    for root in cluster_networks.get_root_nodes(G):
        G.node[root]['label'] = '"R"'
    dot = nx.to_pydot(G).to_string()
    return dot.strip()

@route("/cluster/<cluster>")
@view('templates/network')
def process_cluster(cluster):
    network = get_network_from_cluster(cluster)
    hard = cluster_hard(network)
    subtrees = cluster_networks.potential_number_of_calls(network)
    soft_too_expensive = subtrees > MAX_SUBTREES
    async = not DEBUG
    q = Queue(connection=Redis(), default_timeout=60*15, async=async)
    if not soft_too_expensive:
        soft_job = q.enqueue(cluster_soft, network)
        soft_job_id = soft_job.id
    else:
        soft_job_id = None
    if not cluster_networks.is_treechild(network):
        families_job = q.enqueue(tree_child_families, network)
        families_job_id = families_job.id
    else:
        families_job_id = None
    G = network
    return {
        'cluster': cluster,
        'network_dot': get_dot(G),
        'network_ascii': network.nodes(),
        'network_hard': hard,
        'subtrees': subtrees,
        'queue_key': q.key,
        'soft_job_id': soft_job_id,
        'soft_too_expensive': 1 if soft_too_expensive else 0,
        'families_job_id': families_job_id,
        'is_treechild': cluster_networks.is_treechild(G),
        'number_nodes': len(G.nodes()),
        'number_edges': len(G.edges()),
        'number_hybrids': len(cluster_networks.hybrid_nodes(G)),
        'number_leafs': len(cluster_networks.get_leaf_nodes(G)),
        'number_conflictive_nodes': len(cluster_networks.problematic_treechild_nodes(G)),
        'number_removable_edges': len(cluster_networks.removable_edges(G)),
        'hybridization_degree': cluster_networks.hybridization_degree(G),
    }

###
# Inputs
@post("/input/upload/")
def process_from_upload():
    file_content = request.forms.optionsRadios
    data = request.files.data
    if file_content and data and data.file:
        raw = data.file.read() # This is dangerous for big files
        if file_content == 'cluster':
            return process_clusters(raw)
        elif file_content == 'enewick':
            return process_enewick(raw)
    redirect("/?error=upload")

@post("/input/cluster/")
def process_cluster_post():
    clusters = request.forms.clusters
    return process_clusters(clusters)

def process_clusters(clusters):
    clusters = re.sub("\s+", "", clusters)
    quoted = urllib.quote_plus(clusters)
    redirect("/cluster/"+quoted)

@post("/input/enewick/")
def process_eNewick_post():
    phrase = request.forms.enewick
    return process_enewick(phrase)

def process_enewick(phrase):
    try:
        g = enewick.enewick_to_phylonet(phrase)
    except enewick.MalformedNewickException:
        redirect("/?error=enewick")
    trans = {}
    for node in g.nodes():
        if "#" in node:
            new_node = node.replace("#", "")
            trans[node] = new_node
    nx.relabel_nodes(g, trans, copy=False)
    clusters = re.sub("\s+", "", str(cluster_hard(g)))
    quoted = urllib.quote_plus(clusters)
    redirect("/cluster/"+quoted)

def get_network_from_cluster(cluster):
    if len(cluster) > MAX_QUOTED:
        redirect("/?error=too_long")
    unquoted = urllib.unquote_plus(cluster)
    try:
        clusters = ast.literal_eval(unquoted)
    except SyntaxError:
        redirect("/?error=syntax")
    network = cluster_networks.construct(clusters)
    return network

###
# Downloads
@route("/network/<cluster>/hard/download")
def download_hard(cluster):
    g = get_network_from_cluster(cluster)
    hard = cluster_hard(g)
    s = str(hard)
    r = Response(body=s, status=200)
    r.set_header('Content-Type', 'text/txt')
    r.set_header('Content-Disposition', 'attachment; filename="phylonetwork_soft.txt"')
    return r

@route("/network/<cluster>/soft/download")
def download_soft(cluster):
    g = get_network_from_cluster(cluster)
    async = not DEBUG
    q = Queue(connection=Redis(), default_timeout=60*15, async=async)
    job = q.enqueue(cluster_soft, g)
    for i in range(10):
        if not job.result:
            time.sleep(5)
        else:
            break
    else:
        redirect("/?error='problem generating the file'")
    s = str(job.result)
    r = Response(body=s, status=200)
    r.set_header('Content-Type', 'text/txt')
    r.set_header('Content-Disposition', 'attachment; filename="phylonetwork_soft.txt"')
    return r

###
# Queues and jobs
@route("/job/families/<queue_key>/<job_id>")
def process_job_treechild(queue_key, job_id):
    redis_connection = Redis()
    q = Queue.from_queue_key(queue_key, redis_connection)
    job = q.safe_fetch_job(job_id)
    if job.result != None:
        # This construction may seem weird but the tree-child families may return
        # empty so we cannot just check against «if job.result»
        if not job.result:
            return {'status': 'done', 'value': "", }
        # make web ready and then transform to pydot
        value = [get_dot(g) for g in job.result]
        return {'status': 'done',
                'value': value, }
    else:
        return {'status': 'pending'}

@route("/job/soft/<queue_key>/<job_id>")
def process_job_soft(queue_key, job_id):
    redis_connection = Redis()
    q = Queue.from_queue_key(queue_key, redis_connection)
    job = q.safe_fetch_job(job_id)
    if job.result:
        value =  json.dumps(list(job.result))
        return {'status': 'done',
                'value': value, }
    else:
        return {'status': 'pending'}
###

@route("/")
@view('templates/index')
def repr_network():
    global index_examples
    vals = { 'examples': index_examples, }
    error = request.params.get('error', None)
    if error:
        msg = "Unkown error"
        if error == 'too_long':
            msg = "The input is too long"
        elif error == 'upload':
            msg = "Error during the upload; please check the file content."
        elif error == 'syntax':
            msg = "Incorrect input; please check the syntax"
        elif error == 'enewick':
            msg = "Incorrect eNewick; please check the ending «;»"
        vals['error'] = msg
    return vals

@route("/help")
@view('templates/help')
def help():
    return {}


@route("/about")
@view('templates/about')
def about():
    return {}

@route("/clusters/")
@route("/cluster/")
@route("/input/")
def redirect_main():
    redirect("/")


@route('/static/<filepath:path>')
def server_static(filepath):
        return static_file(filepath, root='./static')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        DEBUG = True
        run(reloader=True, debug=DEBUG, port=8000)
    else:
        run(server='gunicorn', port=8000, workers=5)
