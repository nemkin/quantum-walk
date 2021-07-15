import numpy as np
import scipy.linalg as splinalg
from simulators.coins.coin import Coin


class Hadamard(Coin):

  def start(self):
    return [1/np.sqrt(2), 1j/np.sqrt(2)] + [0 for _ in range(self.size-2)]

  def step(self):
    return splinalg.hadamard(self.size, dtype=complex) / np.sqrt(self.size)

  def describe(self):
    return "Hadamard érme"
