from scipy.sparse import rand

from graphs.subgraphs.SubGraph import SubGraph


class Random(SubGraph):
  edge_probability = 0
  vertexes = []

  def __init__(self, vertexes, edge_probability):
    self.vertexes = list(vertexes)
    self.edge_probability = edge_probability

    N = len(self.vertexes)
    self.edges = rand(N, N, density=edge_probability, format='csr')
    self.edges.data[:] = 1

  def neighbours(self, vertex):
    try:
      index = self.vertexes.index(vertex)
    except ValueError:
      return [vertex]

    neighbour_indices = list(self.edges.getrow(index).nonzero()[1])
    return list(map(lambda ni: self.vertexes[ni], neighbour_indices))

  def describe(self):
    return f"Gráf véletlen élekből {self.edge_probability} valószínűséggel"
