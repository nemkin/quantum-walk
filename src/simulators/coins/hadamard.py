from commands.maths.kronecker_power import kronecker_power
from commands.maths.is_power_of_2 import is_power_of_2
import numpy as np
import scipy.linalg as splinalg
from simulators.coins.coin import Coin
import math


class Hadamard(Coin):

  def start(self):
    return np.array([1/2, -1j/2, -1/2, 1j/2])
    if not is_power_of_2(self.size):
      raise "Nem 2 hatvány a Hadamard érme oldalak száma!"

    exp = int(np.log2(self.size))
    size_2 = np.array([1/np.sqrt(2), 1j/np.sqrt(2)])
    return kronecker_power(size_2, exp)

  def step(self):
    return splinalg.hadamard(self.size, dtype=complex) / np.sqrt(self.size)

  def describe(self):
    return "Hadamard érme"
