import numpy as np
import scipy.linalg as splinalg
from simulators.coins.coin import Coin


class Hadamard(Coin):

  def start(self):
    return np.array([0.5, 0.5j, 0.5, 0.5j] + [0 for _ in range(self.size-4)])

  def step(self):
    return splinalg.hadamard(self.size, dtype=complex) / np.sqrt(self.size)

  def describe(self):
    return "Hadamard érme"
