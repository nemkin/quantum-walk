import numpy as np
from graphs.subgraphs.SubGraph import SubGraph


class Grid(SubGraph):

  def __init__(self, vertexes):
    n = len(vertexes)
    side = int(np.sqrt(n))
    if side ** 2 != n:
      raise "Number of vertexes is not a square number."
    self.vertexes = list(vertexes)

  def neighbours(self, vertex):
    try:
      index = self.vertexes.index(vertex)
    except ValueError:
      return []

    n = len(self.vertexes)
    side = int(np.sqrt(n))

    return list(map(lambda i: self.vertexes[i], filter(lambda i: 0 <= i < n, [index-1, index+side, index+1, index-side])))

  def describe(self):
    return f"Irányítatlan élekből álló grid."
