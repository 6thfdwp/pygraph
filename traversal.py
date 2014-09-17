import sys, os
from graph.xgraph import *
from graph.priority_dict import *


def bfs(G, s=None):
    if s is None:
        s = G.getVertex(0)
    Q = [s] # Q stores the discovered vertices but not further explored yet 
    while Q:
        v = Q.pop(0)
        yield v
        for e in G.adjcent(v):
            source, dest = e['source'], e['dest']
            # if it's start vertex or already discovered or processed 
            # avoid putting this vertex in Q repeatedly 
            if dest == s or dest['predecessor']: 
                continue
            Q.append(dest) # add new to be further explored
            dest['predecessor'] = v


def dfs_norec(G, s=None):
    if s is None:
        s = G.getVertex(0)

def dfs(G, T, s=None):
    """
    Depath first traversal
    """
    if s is None:
        s = G.getVertex(0)
    s['dtime'] = T; T += 1
    print 'visit %s at time %d' % (str(s), s['dtime'])
    for e in G.adjcent(s):
        source, dest = e['source'], e['dest']
        if dest['predecessor']:
            if dest['dtime'] < source['dtime']:
                e['type'] = 'back'
            continue
        dest['predecessor'] = s
        e['type'] = 'tree'
        T = dfs(G, T, dest)
    s['ftime'] = T; T += 1
    print 'finish %s at time %d' % (str(s), s['ftime'])
    return T

def dijkstra(G, s, d):
    """ The single source shortest path on a non-negative weighted graph """

    # Q: key is vertex
    #    value is accumulated cost from 's' to the vertex
    #    priority is the current cost of each vertex

    Q = priority_dict()
    Q[s] = 0.0 # the starting vertex has zero cost
    processed = []
    while Q:
        # extract the vertex with lowest cost so far
        # first u should be starting 's' and then
        value, u = Q.pop_smallest()
        #if u == d:
            #print G.path(d)
        processed.append(u)
        for e in G.adjcent(u):
            dest = e['dest']
            # if dest is already extracted from Q continue next
            if dest in processed:
                continue
            # put the newly discovered vertex in the Q initializing the cost as the maximum 
            Q.setdefault(dest, float('inf'))
            cost = value + e['weight'] # cost by following the edge 'e'
            if cost < Q[dest]: 
                # the dest vertex could be some discovered but not popped from Q yet
                # relax the 'dest' vertex by updating the accumulated cost
                # the newly discovered is always updated

                Q[dest] = cost
                # there is a shorter path from u 
                dest['predecessor'] = u

if __name__ == '__main__':
    conf = os.getcwd() + '/conf/' + sys.argv[1]
    #conf = os.getcwd() + '/graph/graph1.txt'
    #G = UndirectedGraph(conf)
    G = DirectedGraph(conf)
    T = 1
    dfs(G, T)
    #for v in dfs_nonrec(G, G.getVertex(0)):
        #print v
    #for v in bfs(G):
        #print v
