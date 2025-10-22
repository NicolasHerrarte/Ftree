import numpy as np
class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.vertex_amount = 0
        self.edge_amount = 0

    def addVertices(self, amount):
        for i in range(amount):
            new_vertex = Vertex(self.vertex_amount,{})
            self.vertices.append(new_vertex)
            self.vertex_amount += 1


    def addEdge(self, id_edge):
        object_edge = Edge(self.vertices[id_edge[0]], self.vertices[id_edge[1]])
        self.edge_amount += 1
        self.edges.append(object_edge)

    def getEdgesId(self):
        return [x.getIdConnection() for x in self.edges]

    def getAdjMatrix(self):
        id_edges = self.getEdgesId()
        adj_matrix = np.zeros((self.vertex_amount, self.vertex_amount))
        for e in id_edges:
            adj_matrix[e[0], e[1]] = 1
            adj_matrix[e[1], e[0]] = 1
        return adj_matrix

    def getVerticesDegree(self):
        return np.sum(self.getAdjMatrix(), axis=1)

class Vertex:
    def __init__(self, id, framework):
        self.id = id
        self.framework = framework.copy()

class Edge:
    def __init__(self, v1, v2):
        self.connection = (v1, v2)

    def getIdConnection(self):
        return (self.connection[0].id, self.connection[1].id)

graph = Graph()
graph.addVertices(6)
graph.addEdge((0,1))
graph.addEdge((1,2))
graph.addEdge((1,5))
graph.addEdge((2,3))
graph.addEdge((2,5))
graph.addEdge((3,4))
graph.addEdge((3,5))
graph.addEdge((4,5))

print(graph.getEdgesId())
print(graph.getAdjMatrix())
print(graph.getVerticesDegree())

