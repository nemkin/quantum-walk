import random
import sys
import traceback

from tqdm import tqdm

import numpy as np

from simulators.simulator import Simulator


class Quantum(Simulator):

  def probability(probability_amplitudes):
    return probability_amplitudes.real**2 + probability_amplitudes.imag**2

  def simulate(graph, start, simulations, steps):

    N = graph.vertex_count()

    for _ in tqdm(range(simulations), leave=False):

      pos_0 = np.zeros(N, dtype=complex)
      pos_1 = np.zeros(N, dtype=complex)
      pos_0[start] = 1 / np.sqrt(2)
      pos_1[start] = 1j / np.sqrt(2)

      currpos_0 = pos_0
      currpos_1 = pos_1
      counts = np.zeros((1, N), dtype=float)
      counts[0, start] = 1

      for _ in tqdm(range(steps), leave=False):
        nextpos_0 = np.zeros(N, dtype=complex)
        nextpos_1 = np.zeros(N, dtype=complex)
        for i in tqdm(range(N), leave=False):
          n1, n2 = graph.neighbours(i)  # Must have 2 neighbours.

          nextpos_0[n2] += (currpos_0[i] + currpos_1[i]) / np.sqrt(2)
          nextpos_1[n1] += (currpos_0[i] - currpos_1[i]) / np.sqrt(2)

        currpos_0 = nextpos_0
        currpos_1 = nextpos_1

        probabilities = Quantum.probability(
            currpos_0) + Quantum.probability(currpos_1)

        counts = counts = np.concatenate(
            (counts, np.array([probabilities])), axis=0)

    return counts

  def describe():
    return "Kvantum szimuláció"
