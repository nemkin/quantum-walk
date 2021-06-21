import itertools
import numpy as np


class Graph(object):

  def __init__(self, sub_graphs):
    self.sub_graphs = list(sub_graphs)

  def vertex_count(self):
    max_vertexes = map(lambda sub_graph: max(
        sub_graph.vertexes), self.sub_graphs)
    return max(max_vertexes)+1

  def neighbours(self, vertex):
    return sorted(list(set(list(itertools.chain.from_iterable(map(lambda sub_graph: sub_graph.neighbours(vertex), self.sub_graphs))))))

  def adjacency_matrix(self):
    N = self.vertex_count()
    adjacencies = list(map(lambda sg: sg.adjacency_matrix(N),
                           self.sub_graphs))

    return np.sum(adjacencies, 0)
