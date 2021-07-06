import numpy as np


class Tester:
  def __init__(self, run):
    self.run = run

  def is_permuation_matrix(matrix):
    matrix = np.asanyarray(matrix)
    if matrix.ndim != 2:
      return False
    if matrix.shape[0] != matrix.shape[1]:
      return False
    if not ((matrix == 1) | (matrix == 0)).all():
      return False
    if not (matrix.sum(axis=0) == 1).all():
      return False
    if not (matrix.sum(axis=1) == 1).all():
      return False
    return True

  def test(self):
    for index, coin_face in enumerate(self.run.coin_faces):
      if not Tester.is_permuation_matrix(coin_face):
        raise Exception(
            f"Run {self.run.filename}: Coin face #{index} is not a permutation matrix!")
