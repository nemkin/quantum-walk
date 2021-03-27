class Graph(object):
    sub_graphs = []

    def neighbours(self, vertex):
        return list(set(map(lambda sub_graph: sub_graph.neighbours(vertex), self.sub_graphs)))
