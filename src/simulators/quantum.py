import random
import sys
import traceback

from tqdm import tqdm

import numpy as np

from simulators.simulator import Simulator


class Quantum(Simulator):

  def probability(probability_amplitudes):
    print(probability_amplitudes)
    return (probability_amplitudes.real**2 + probability_amplitudes.imag**2).sum(axis=1)

  def coin(size):
    return np.array(([1, 1], [1, -1])) / np.sqrt(2)

  def simulate(graph, start, simulations, steps):

    N = graph.vertex_count()
    max_neighbour_count = int(graph.adjacency_matrix().sum(axis=0).max())
    print(max_neighbour_count)
    for _ in tqdm(range(simulations), leave=False):

      pos = np.zeros((N, max_neighbour_count), dtype=complex)
      pos[start, 0] = 1

      currpos = pos
      counts = np.zeros((1, N), dtype=float)
      counts[0, start] = 1

      for _ in tqdm(range(steps), leave=False):
        nextpos = np.zeros((N, max_neighbour_count), dtype=complex)
        for i in tqdm(range(N), leave=False):
          n = graph.neighbours(i)
          n = sorted(n + [i]*(max_neighbour_count-len(n)))
          print(i)
          print(n)
          for index, multiplicators in enumerate(Quantum.coin(max_neighbour_count)):
            nextpos[n[index],
                    index] += currpos[i].dot(np.squeeze(multiplicators))

        currpos = nextpos

        probabilities = Quantum.probability(currpos)

        counts = counts = np.concatenate(
            (counts, np.array([probabilities])), axis=0)

    return counts

  def describe():
    return "Kvantum szimuláció"
