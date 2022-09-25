import numpy as np


def matrix2string(m):
  return np.array2string(m, max_line_width=200, precision=2)
