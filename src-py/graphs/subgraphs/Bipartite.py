from graphs.subgraphs.SubGraph import SubGraph


class Bipartite(SubGraph):

  def __init__(self, side_a, side_b):
    self.side_a = list(side_a)
    self.side_b = list(side_b)
    self.vertexes = list(self.side_a + self.side_b)

  def neighbours(self, vertex):
    if vertex in self.side_a:
      return self.side_b
    if vertex in self.side_b:
      return self.side_a
    return []

  def describe(self):
    return f"Teljes páros gráf"
