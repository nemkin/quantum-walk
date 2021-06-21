import random
import sys
import traceback

from tqdm import tqdm

import numpy as np

from simulators.simulator import Simulator


class Quantum(Simulator):

  def simulate(graph, start, simulations, steps):

    N = graph.vertex_count()

    for _ in tqdm(range(simulations), leave=False):

      pos_0 = np.zeros(N, dtype=complex)
      pos_0[start] = 1
      pos_1 = np.zeros(N, dtype=complex)

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
          print(
              f"{n2}, {currpos_0[i]} + {currpos_1[i]} / sqrt(2) = {nextpos_0[n2]}")
          print(
              f"{n1}, {currpos_0[i]} - {currpos_1[i]} / sqrt(2) = {nextpos_1[n1]}")
          print("---")
        currpos_0 = nextpos_0
        currpos_1 = nextpos_1
        print("NEW LINE ---------------------------------------------------")
        probabilities = np.absolute(currpos_0) + np.absolute(currpos_1)

        counts = counts = np.concatenate(
            (counts, np.array([probabilities])), axis=0)

    return counts

  def describe():
    return "Kvantum szimuláció"
