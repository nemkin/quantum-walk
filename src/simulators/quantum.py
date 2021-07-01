import sys
import numpy as np
from scipy import linalg as splinalg
from tqdm import tqdm

from simulators.simulator import Simulator


class Quantum(Simulator):

  def probability(probability_amplitudes):
    return (probability_amplitudes.real**2 + probability_amplitudes.imag**2).sum(axis=1)

  def coin_start_state(size):
    return [1/np.sqrt(2), 1j/np.sqrt(2)] + [0]*(size-2)

  def coin(size):
    return splinalg.dft(size) / np.sqrt(size)

  def simulate(graph, start, simulations, steps):

    N = graph.vertex_count()
    regularity = graph.max_degree()
    coin = Quantum.coin(regularity)

    for _ in tqdm(range(simulations), leave=False):

      pos = np.zeros((N, regularity), dtype=complex)
      pos[start] = Quantum.coin_start_state(regularity)

      currpos = pos
      counts = np.zeros((1, N), dtype=float)
      counts[0, start] = 1

      for _ in tqdm(range(steps), leave=False):
        nextpos = np.zeros((N, regularity), dtype=complex)
        for i in tqdm(range(N), leave=False):
          n = graph.neighbours(i)
          for index, multiplicators in enumerate(coin):
            nextpos[n[index],
                    index] += currpos[i].dot(np.squeeze(multiplicators))

        currpos = nextpos

        probabilities = Quantum.probability(currpos)

        counts = counts = np.concatenate(
            (counts, np.array([probabilities])), axis=0)

    return counts

  def describe():
    return "Kvantum szimuláció"
