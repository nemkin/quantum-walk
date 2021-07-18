import numpy as np
import scipy as sp
from simulators.coins.coin import Coin


class Dft(Coin):

  def start(self):
    return np.array([1/np.sqrt(2), 1j/np.sqrt(2)] + [0 for _ in range(self.size-2)])

  def step(self):
    return sp.linalg.dft(self.size) / np.sqrt(self.size)

  def describe(self):
    return "DFT érme"
