from graph.base import *
import os

class UndirectedGraph(GraphAdj):
    def addEdge(self, sindex, dindex, weight):
        #super(UndirectedGraph, self).addEdge(self, sindex, dindex, weight)
        edge = GraphAdj.addEdge(self, sindex, dindex, weight)
        self.getVEntry(edge['source']).edges.append(edge)
        self.getVEntry(edge['dest']).edges.append(edge.reverse())
        return edge


class DirectedGraph(GraphAdj):
    def addEdge(self, sindex, dindex, weight):
        #super(DirectedGraph, self).addEdge(self, sindex, dindex, weight)
        edge = GraphAdj.addEdge(self, sindex, dindex, weight)
        self.getVEntry(edge['source']).edges.append(edge)
        return edge

if __name__ == '__main__':
    conf = os.getcwd() + '/conf/graph0.txt'
    G = DirectedGraph(conf)
    G.output()
    G1 = UndirectedGraph(conf)
    G1.output()
