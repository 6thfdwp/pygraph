import sys, os
from graph.xgraph import *


def bfs(G, s=None):
    if s is None:
        s = G.getVertex(0)
    Q = [s] # vertices discovered but not processed yet 
    while Q:
        v = Q.pop(0)
        yield v
        for e in G.adjcent(v):
            source, dest = e['source'], e['dest']
            # if it's start vertex or already discovered or processed 
            if dest == s or dest['predecessor']: 
                continue
            Q.append(dest) # add new to be further explored
            dest['predecessor'] = v


def dfs_norec(G, s=None):
    if s is None:
        s = G.getVertex(0)

if __name__ == '__main__':
    conf = os.getcwd() + '/conf/' + sys.argv[1]
    #conf = os.getcwd() + '/graph/graph1.txt'
    G = UndirectedGraph(conf)
    #G = DirectedGraph(conf)
    #for v in dfs_nonrec(G, G.getVertex(0)):
        #print v
    for v in bfs(G):
        print v
