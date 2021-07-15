import numpy as np
import scipy as sp
from simulators.coins.coin import Coin


class Grover(Coin):

  def start(self):
    if self.size == 2:
      return [1/np.sqrt(2), 1j/np.sqrt(2)]
    if self.size == 4:
      return [1/2, 1j/2, -1/2, -1j/2]
    raise f"Grover coin nincs definiálva ${self.size} méretre!"

  def step(self):
    ones = np.ones((self.size, self.size), dtype=complex)
    diag_ones = np.identity(self.size, dtype=complex)
    return (2/self.size * ones) - diag_ones

  def describe(self):
    return "Grover érme"
