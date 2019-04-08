"""
Simple graph implementation
"""


class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):  #  takes 2 vertices and creates an edge between them
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)  #  add an edge from v1 to v2
            self.vertices[v2].add(v1)  #  add an edge from v2 to v1
        else:
            raise IndexError("One of those vertices does not exist")
