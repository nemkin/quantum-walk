from commands.maths.kronecker_power import kronecker_power
from commands.maths.is_power_of_2 import is_power_of_2
import numpy as np
import scipy as sp
from simulators.coins.coin import Coin


class Grover(Coin):

  def start(self):
    if not is_power_of_2(self.size):
      raise "Nem 2 hatvány a Grover érme oldalak száma!"

    exp = int(np.log2(self.size))
    size_2 = np.array([1/np.sqrt(2), 1j/np.sqrt(2)])
    return kronecker_power(size_2, exp)

  def step(self):
    ones = np.ones((self.size, self.size), dtype=complex)
    diag_ones = np.identity(self.size, dtype=complex)
    return (2/self.size * ones) - diag_ones

  def describe(self):
    return "Grover coin"
