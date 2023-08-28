import numpy as np


def is_unitary(m):
  return np.allclose(np.eye(m.shape[0]), m.dot(m.T.conj()))
