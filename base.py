class Vertex:
    """
     Vertex Class represents a vertex in graph
    """
    #__slots__ = ['index', 'label', 'predecessor', 'status']
    def __init__(self, label):
        """
        Initialize vertex's attributes
        index -- Self incremental integer storing its index in the whole graph
        lable -- String name representing this vertex
        
        Temporary attributes used in graph traversal
        predecessor (Vertex) -- Vertex's predecessor
        dtime (int)          -- Discovered time in dfs
        ftime (int)          -- Finisheed time in dfs
        cost  (float)        -- Cost to reach this vertex in Dijkstra
        """
        self.index = -1
        self.label = label

        self.predecessor = None
        self.dtime = -1
        self.ftime = -1
        self.cost = float('inf')
        self.status = ()
    
    def __getitem__(self, key):
        """
        Protocal for dict style get 
        Eg. vertex['index']
        """
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
        """
        Protocol for dict style set 
        Eg. vertex['index'] = index
        """
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
        """
        Initialize Edge attributes
        source (Vertex)      -- The source vertex (one end) of the edge
        destination (Vertex) -- The destination vertex (the other end) of the edge
        weight (float)       -- The weight of the edge, default is 1.0 in unweighted graph
        """
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
    """
    Graph class using adjacent representation 

    It contains a list of vertices each of which has 
    a list edges representing its connection with other vertices
    """
    def __init__(self, conf=None):
        """
        Initialize
        vertices (list) -- All the Vertex instances contained
        curIndex (int)  -- Current iterating vertex's index in the graph
        """
        self.vertices = []
        self.curIndex = -1
        if conf is not None:
            self.setup(conf)
    
    def setup(self, conf):
        """
        Set up the graph with a conf file
        It has the following format:

        a b c d e # the label of each vertex 
        0 1 21    # an edge between vertex 0 (a) and 1 (b) with weight as 21
        0 2 55    # an edge between vertex 0 (a) and 2 (c) with weight as 55
        ...
        """
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
        """
        Internal class representing a vertex and its edges
        """
        def __init__(self, v):
            self.vert = v
            self.edges = []

        # def __str__(self):
        #     return str(self.vert)
    class EdgeIter:
        """
        Internal class for iterator of a vertex's edges
        """
        def __init__(self, v, graph):
            self.graph = graph
            self.edgesTo = graph.getVEntry(v).edges

        def __iter__(self):
            """
            Make edges iterable using for .. in syntax
            """
            return iter(self.edgesTo)

    def addVertex(self, v):
        v['index'] = self.size()
        self.vertices.append(GraphAdj.VEntry(v))

    def addEdge(self, sindex, dindex, weight):
        """
        Add an edge to link source to destination vertex
        Only create Edge instance in the base class, since for
        undirected and directed graph it has different ways to 
        add the edge in both connected vertices

        @param sindex (int)   -- The index of source vertex
        @param dindex (int)   -- The index of destination vertex
        @param weight (float) -- The weight of the edge

        @return Edge instance
        """
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
        """
        The number of outgoing edges of the vertex

        @return int 
        """
        return len(self.getVEntry(v).edges)

    """ 
    Protocol to make the graph iterable over its vertices list
    using for ... in syntax
    """
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

    def adjcent(self, u):
        """
        Visit the adjcent nodes of a vertex

        @return iterator to loop the edge list of a vertex
        """
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
