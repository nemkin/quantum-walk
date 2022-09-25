import numpy as np


class SubGraph(object):

  def neighbours(self, vertex):
    return []

  def describe(self):
    return "Ismeretlen részgráf"

  def adjacency_matrix(self, vertex_count):
    adjacency = np.zeros([vertex_count, vertex_count])

    for i in range(vertex_count):
      neighbours = self.neighbours(i)
      for j in neighbours:
        adjacency[j, i] += 1

    return adjacency
