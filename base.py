class Vertex:
    #__slots__ = ['index', 'label', 'predecessor', 'status']
    def __init__(self, label):
        self.index = -1
        self.label = label

        self.predecessor = None
        self.dtime = -1
        self.ftime = -1
        self.cost = float('inf')
        self.status = ()

    def __getitem__(self, key):
        if key == 'index':
            return self.index
        elif key == 'label':
            return self.label
        elif key == 'predecessor':
            return self.predecessor
        elif key == 'dtime':
            return self.dtime
        elif key == 'ftime':
            return self.ftime

    def __setitem__(self, key, value):
        if key == 'index':
            self.index = value
        elif key == 'label':
            self.label = value
        elif key == 'predecessor':
            self.predecessor = value
        elif key == 'dtime':
            self.dtime= value
        elif key == 'ftime':
            self.ftime = value

    def __hash__(self):
        return hash(self.index)
    def __eq__(self, other):
        return self.index == other.index

    def __repr__(self):
        # return '%s_%s(%d)' % (self.__class__.__name__, self.label, self.index)
        return self.label
    def __str__(self):
        return '%s[%f]' % (self.label, self.cost)

class Edge:
    def __init__(self, source, destination, weight=1.0):
        self.source = source
        self.destination = destination
        self.weight = weight

    def __getitem__(self, key):
        if key == 'source':
            return self.source
        elif key == 'dest':
            return self.destination
        elif key == 'weight':
            return self.weight
        elif key == 'type':
            return self.type

    def __setitem__(self, key, value):
        if key == 'weight':
            self.weight = value
        elif key == 'type':
            self.type = value

    def reverse(self):
        return Edge(self.destination, self.source, self.weight)

    def __str__(self):
        return '%s->%s [%d]' % (str(self.source), str(self.destination), self.weight)

class GraphAdj:
    def __init__(self, conf=None):
        self.vertices = []
        self.curIndex = -1
        if conf is not None:
            self.setup(conf)
    
    def setup(self, conf):
        f = open(conf)
        for i, line in enumerate(f):
            items = line.split(' ')
            if i == 0:
                for item in items:
                    self.addVertex(Vertex( item.strip() ))
                continue
            try:
                weight = float(items[2])
            except IndexError:
                weight = 1.0
            sindex, dindex = items[0], items[1]
            self.addEdge(sindex, dindex, weight)

    def output(self):
        print "initial graph: \n",
        for u in self:
            for e in self.adjcent(u):
                print e

    class VEntry:
        def __init__(self, v):
            self.vert = v
            self.edges = []

        # def __str__(self):
        #     return str(self.vert)
    class EdgeIter:
        def __init__(self, v, graph):
            self.graph = graph
            self.edgesTo = graph.getVEntry(v).edges

        def __iter__(self):
            return iter(self.edgesTo)

    def addVertex(self, v):
        v['index'] = self.size()
        self.vertices.append(GraphAdj.VEntry(v))

    def addEdge(self, sindex, dindex, weight):
        sindex, dindex = int(sindex), int(dindex)
        try:
            source = self.getVertex(sindex)
            dest = self.getVertex(dindex)
            newedge = Edge(source, dest, weight)
            return newedge
        except IndexError:
            print "vertex indext error"

    def getVertex(self, index):
        try:
            result = self.vertices[index].vert
        except IndexError:
            result = None
        return result

    def getVEntry(self, v):
        return self.vertices[v['index']]

    def size(self):
        return len(self.vertices)

    def degree(self, v):
        return len(self.getVEntry(v).edges)

    # iterate each node in graph
    def next(self):
        self.curIndex += 1
        try:
            #result = self.getVertex(self.curIndex)
            result = self.vertices[self.curIndex].vert
        except IndexError:
            self.curIndex = -1
            raise StopIteration
        return result
    def __iter__(self):
        #vlist = [each.vert for each in self.vertices]
        #return iter(vlist)
        return self

    # iterator for a vertex's out edges to explore its adjcent nodes
    def adjcent(self, u):
        return self.EdgeIter(u, self)

    def path(self, dest):
        pre = dest['predecessor']
        if pre is None:
            return [dest]
        return self.path(pre) + [dest]

if __name__ == '__main__':
    G = GraphAdj()
    for i in range(5):
        G.addVertex( Vertex('a'+str(i)) )
    #for u in G:
        #print '...'
    #v1 = Vertex('a')
    #v2 = Vertex('b')
    #print v1['label']
    #print v2['label']
    #v2['label'] = 'c'
