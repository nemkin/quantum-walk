import numpy as np
from graphs.subgraphs.SubGraph import SubGraph


class Grid(SubGraph):

  def __init__(self, vertexes):
    self.n = len(vertexes)
    self.side = int(np.sqrt(self.n))
    if self.side ** 2 != self.n:
      raise "Number of vertexes is not a square number."
    self.vertexes = list(vertexes)

  def row(self, index):
    return index // self.side

  def left(self, index):
    # row = index // self.side
    # col = index % self.side

    # new_col = (col-1) % self.side
    # return row*self.side + new_col
    if self.row(index) == self.row(index-1):
      return index-1
    else:
      return index + self.side - 1

  def right(self, index):
    if self.row(index) == self.row(index+1):
      return index+1
    else:
      return index - self.side + 1

  def top(self, index):
    return (index + self.side) % self.n

  def bottom(self, index):
    return (index - self.side) % self.n

  def neighbours(self, vertex):
    try:
      index = self.vertexes.index(vertex)
    except ValueError:
      return []

    return list(
        map(
            lambda i: self.vertexes[i],
            [
                self.top(index),
                self.bottom(index),
                self.left(index),
                self.right(index)
            ]
        )
    )

  def describe(self):
    return f"Irányítatlan élekből álló grid."
