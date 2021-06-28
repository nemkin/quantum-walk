import random

import numpy as np
import progressbar
from scipy.linalg import hadamard


np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=np.inf)


class Quantum():

  # http://susan-stepney.blogspot.com/2014/02/mathjax.html

  def measure(N, psii):
    prob = np.empty(N)
    for k in range(N):
      posn = np.zeros(N)
      posn[k] = 1
      M_hat_k = np.kron(np.outer(posn, posn), np.eye(2))
      proj = M_hat_k.dot(psii)
      prob[k] = proj.dot(proj.conjugate()).real
    return prob

  def simulate(graph, start, simulations, steps):

    with open("../generations/old_simulator.txt", "wb") as f:

      N = graph.vertex_count()

      coin0 = np.array([1, 0])  # |0>
      coin1 = np.array([0, 1])  # |1>

      C00 = np.outer(coin0, coin0)  # |0><0|
      C01 = np.outer(coin0, coin1)  # |0><1|
      C10 = np.outer(coin1, coin0)  # |1><0|
      C11 = np.outer(coin1, coin1)  # |1><1|

      C_hat = (C00 + C01 + C10 - C11)/np.sqrt(2.)

      ShiftPlus = np.roll(np.eye(N), 1, axis=0)
      ShiftMinus = np.roll(np.eye(N), -1, axis=0)
      S_hat = np.kron(ShiftPlus, C00) + np.kron(ShiftMinus, C11)

      U = S_hat.dot(np.kron(np.eye(N), C_hat))

      for _ in progressbar.progressbar(range(simulations)):

        pos = np.zeros(N)
        pos[start] = 1
        psi0 = np.kron(pos, (coin0 + coin1 * 1j) / np.sqrt(2.))
        counts = np.array([Quantum.measure(N, psi0)])

        out = [psi0]
        for step_i in range(1, steps + 1):
          psii = np.linalg.matrix_power(U, step_i).dot(psi0)
          out = np.concatenate((out, np.array([psii])), axis=0)
          prob = Quantum.measure(N, psii)

        # TODO options = graph.neighbours(pos)
          counts = np.concatenate((counts, np.array([prob])), axis=0)

      np.save(f, out)
    return counts

  def describe():
    return "Kvantum szimuláció"
