import numpy as np


def kronecker_power(matrix, power):
  result = matrix.copy()
  for i in range(power-1):
    result = np.kron(result, matrix)
  return result
