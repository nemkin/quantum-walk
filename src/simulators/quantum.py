import numpy as np
from tqdm import tqdm

from simulators.simulator import Simulator


class Quantum(Simulator):

  def __init__(self, coin, start, simulations, steps):
    self.coin = coin
    self.start = start
    self.simulations = simulations
    self.steps = steps

  def probability(probability_amplitudes):
    return (probability_amplitudes.real**2 + probability_amplitudes.imag**2).sum(axis=1)

  def simulate(self, graph):

    N = graph.vertex_count()
    regularity = graph.max_degree()
    self.coin.set_size(regularity)
    coin_step = self.coin.step()

    for _ in tqdm(range(self.simulations), desc=f"{graph.name}: {self.describe()} simulations", leave=False):

      pos = np.zeros((N, regularity), dtype=complex)
      pos[self.start] = self.coin.start().copy()

      currpos = pos.copy()
      counts = np.zeros((1, N), dtype=float)
      counts[0, self.start] = 1

      for _ in tqdm(range(self.steps), desc=f"{graph.name}: {self.describe()} steps", leave=False):
        nextpos = np.zeros((N, regularity), dtype=complex)
        for i in tqdm(range(N), desc=f"{graph.name}: {self.describe()} vertexes", leave=False):
          n = graph.neighbours(i)
          # TODO: ez itt sor vagy oszlop?
          for index, multiplicators in enumerate(coin_step):
            nextpos[n[index],
                    index] += currpos[i].dot(multiplicators)
        currpos = nextpos.copy()
        probabilities = Quantum.probability(currpos)
        counts = np.concatenate(
            (counts, np.array([probabilities])), axis=0)

    return counts

  def is_quantum(self):
    return True

  def describe(self):
    return f"Quantum simulation ({self.coin.describe()})"
