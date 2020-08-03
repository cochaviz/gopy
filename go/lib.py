class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbour(self, neighbour, weight=0):
        self.adjacent[neighbour] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbour):
        return self.adjacent[neighbour]

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def add_vert_with_neighbours(self, node, neighbours):
        self.add_vertex(node)

        for neighbour in neighbours:
            if neighbour not in self.vert_dict:
                self.add_vertex(neighbour)

            self.add_edge(neighbour, node)

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbour(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbour(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()
    
    def get_vertices_with_less_than_n_neighbours(self, n):
        verts = []

        for vert in self.vert_dict.keys():
            current_vertex = self.get_vertex(vert)
            if len(current_vertex.get_connections()) < n:
                verts.append(vert)

        return verts

class Utils:
    @staticmethod
    def merge(a, b, merge_vert, neighbours):
        new_graph = Graph()
        new_graph.vert_dict = {**a.vert_dict, **b.vert_dict}
        new_graph.num_vertices = a.num_vertices + b.num_vertices
        new_graph.add_vertex(merge_vert)

        for neighbour in neighbours:
            new_graph.add_edge(neighbour, merge_vert)

        return new_graph


