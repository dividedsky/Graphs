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

    def add_directed_edge(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("One of those vertices does not exist")

    def bft(self, starting_vertex):
        q = []  # replace with queue later
        q.append(starting_vertex)
        visited = set()
        while len(q) > 0:
            v = q.pop(0)
            if v not in visisted:
                visited.add(v)
                print(v)
                for vert in self.vertices[v]:
                    # add all of this vert's neighbors to queue
                    q.append(vert)

    def dft(self, starting_vertex):
        s = []  # replace with stack later?
        s.append(starting_vertex)
        visited = set()
        while len(s) > 0:
            v = s.pop()
            print(v)
            visited.add(v)
            for vert in self.vertices[v]:
                if vert not in visited:
                    s.append(vert)

    def dft_recursive(self, starting_vertex, visited=None):
        if visited is None:
            visited = set()
        print(starting_vertex)
        visited.add(starting_vertex)
        if len(self.vertices[starting_vertex]) == 0:
            return
        else:
            for v in self.vertices[starting_vertex]:
                if v not in visited:
                    self.dtf_recursive(v, visited)

    def bft_search(self, starting_vertex, target):
        q = []
        q.append([starting_vertex])
        visited = set()
        while len(q) > 0:
            v = q.pop(0)
            print("searching", v)
            if v[-1] not in visited:
                visited.add(v[-1])
                if v[-1] == target:
                    print(f"found {target}. shortest path is {v}")
                    return True
                else:
                    for vert in self.vertices[v[-1]]:
                        path = v.copy()
                        path.append(vert)
                        q.append(path)
        return False

    def dft_search(self, starting_vertex, target):
        s = []
        s.append([starting_vertex])
        visited = set()
        while len(s) > 0:
            v = s.pop()
            if v[-1] not in visited:
                visited.add(v[-1])
                if v[-1] == target:
                    print(f"fount {target} through path {v}")
                    return True
                else:
                    for vert in self.vertices[v[-1]]:
                        path = v.copy()
                        path.append(vert)
                        s.append(path)

    def dfs_r(self, start, target, visited=None, path=None):
        if visited is None:
            visited = set()
        if path is None:
            path = []
        visited.add([start])
        path = parth + [start]
        if start == target:
            return path
        for child in self.vertices[start]:
            if child not in visited:
                new_path = self.dfs_r(child, target, visited, path)
                if new_path:
                    return new_path
        return None


graph = Graph()
graph.add_vertex("0")
graph.add_vertex("1")
graph.add_vertex("2")
graph.add_vertex("3")
graph.add_vertex("4")
graph.add_vertex("5")
graph.add_edge("0", "1")
graph.add_edge("1", "2")
graph.add_edge("0", "3")
graph.add_edge("3", "4")
graph.add_edge("4", "5")
print(graph.vertices)
# print(graph.bft("0"))
# print(graph.dft("0"))
# print(graph.dft_recursive("0"))
print(graph.bft_search("0", "4"))
print(graph.dft_search("0", "5"))
