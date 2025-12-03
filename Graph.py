import numpy as np
from Tree import Tree
from collections import deque

class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.vertex_amount = 0
        self.edge_amount = 0

    def addVertices(self, amount, vertex_framework):
        added_vertices = []
        for i in range(amount):
            new_vertex = Vertex(self.vertex_amount,vertex_framework)

            added_vertices.append(new_vertex)
            self.vertices.append(new_vertex)
            self.vertex_amount += 1

        if amount == 1:
            return added_vertices[0]

        return added_vertices

    def vertices_ids(self):
        return [x.id for x in self.vertices]

    def vertex_object_from_id(self, object_id):
        for o in self.vertices:
            if o.id == object_id:
                return o

    def vertex_object_from_attr(self, object_attr, attr_value):
        for o in self.vertices:
            if o.get_value(object_attr) == attr_value:
                return o

    def vertex_connections(self, object):
        connections = []
        for e in self.edges:
            if e.connection[0].is_equal(object):
                connections.append(e.connection[1])

        return connections

    def addEdge(self, id_edge):
        object_edge = Edge(self.vertices[id_edge[0]], self.vertices[id_edge[1]])
        self.edge_amount += 1
        self.edges.append(object_edge)
        return object_edge

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

    def BFS_tree(self, start_object, search_element=None, max_search_depth=None, unpack=False):

        # THIS NEEDS TO BE REPLACED NOW
        def last_minute_recursive_print(tree, location):
            s = ""
            insp = []
            for i in location:
                #print(insp)
                #print(tree.findNode(insp).getValue("Vertex"))
                s += tree.findNode(insp).getValue("Vertex")["value"]["First Name"]
                s += " -> "
                insp.append(i)

            s += tree.findNode(insp).getValue("Vertex")["value"]["First Name"]
            #print(s)
            #print(insp)

            return s


        frame = {
            "Vertex": None
        }
        bsf_tree = Tree(frame)
        main_node = bsf_tree.main_node
        main_node.setValue(start_object, "Vertex")

        visited = [False] * len(self.vertices)
        visited[start_object.id] = True

        queue = deque()
        queue.append(main_node)


        while queue:
            curr = queue.popleft()
            conns = self.vertex_connections(curr.getValue("Vertex"))

            if unpack:
                curr.unpackValue("Vertex")
            for c in conns:
                if not visited[c.id]:
                    visited[c.id] = True
                    new_child = curr.addChild()
                    new_child.setValue(c, "Vertex")
                    if max_search_depth is not None and new_child.getValue("Depth") > max_search_depth:
                        return bsf_tree, -1, None

                    if search_element is not None and c.is_equal(search_element):
                        new_child.unpackValue("Vertex")
                        return bsf_tree, new_child.getValue("Depth"), last_minute_recursive_print(bsf_tree,new_child.location.location)

                    queue.append(new_child)

        return bsf_tree, -1, None


class Vertex:
    def __init__(self, _id, framework):
        self.id = _id
        self.framework = framework.copy()
        self.value = framework.copy()

    def set_value(self, dict_key, new_value):
        self.value[dict_key] = new_value

    def get_value(self, dict_key):
        return self.value[dict_key]

    def unpack(self):
        return {"id": self.id, "value": self.value}

    def is_equal(self, vertex):
        if vertex.id == self.id:
            return True

    def __str__(self):
        return str({"id":self.id,
                    "value":self.value})

class Edge:
    def __init__(self, v1, v2):
        self.connection = (v1, v2)

    def getIdConnection(self):
        return self.connection[0].id, self.connection[1].id

