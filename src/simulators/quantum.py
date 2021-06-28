import sys
import numpy as np
from scipy import linalg as splinalg
from tqdm import tqdm

from simulators.simulator import Simulator


np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=np.inf)


class Quantum(Simulator):

  def probability(probability_amplitudes):
    return (probability_amplitudes.real**2 + probability_amplitudes.imag**2).sum(axis=1)

  def coin_start_state(size):
    return np.array([1/np.sqrt(2), 1j/np.sqrt(2)] + [0]*(size-2))

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

      out = [currpos.flatten()]
      for _ in tqdm(range(steps), leave=False):
        nextpos = np.zeros((N, regularity), dtype=complex)
        for i in tqdm(range(N), leave=False):
          n = graph.neighbours(i)
          # Ha ez nem sorted hanem random (egyszer balra/egyszer jobbra) akkor nagyon más jön ki!
          n = sorted(n + [i]*(regularity-len(n)))
          for index, multiplicators in enumerate(coin):
            nextpos[n[index],
                    index] += currpos[i].dot(np.squeeze(multiplicators))

        currpos = nextpos
        out = np.concatenate((out, np.array([currpos.flatten()])), axis=0)

        probabilities = Quantum.probability(currpos)

        counts = counts = np.concatenate(
            (counts, np.array([probabilities])), axis=0)

    with open("../generations/new_simulator.txt", "wb") as f:
      np.save(f, out)

    return counts

  def describe():
    return "Kvantum szimuláció"
