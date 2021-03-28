from graphs.subgraphs.SubGraph import SubGraph


class Bipartite(SubGraph):
  side_a = []
  side_b = []
  vertexes = []

  def __init__(self, side_a, side_b):
    self.side_a = list(side_a)
    self.side_b = list(side_b)
    self.vertexes = self.side_a + self.side_b

  def neighbours(self, vertex):
    if vertex in self.side_a:
      return self.side_b
    if vertex in self.side_b:
      return self.side_a
    return [vertex]
