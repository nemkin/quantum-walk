import numpy as np
import itertools


class Eigens:
  def __init__(self, adj):
    self.adj = adj
    self.eigen_values, self.eigen_vectors = np.linalg.eig(adj)

  def get_eigen_values(self):
    return list(set(self.eigen_values))

  def get_eigen_vectors_for(self, eigen_value):
    return self.eigen_vectors[self.eigen_values == eigen_value]
