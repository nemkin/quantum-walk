import random
import sys
import traceback

from tqdm import tqdm

import numpy as np

from simulators.simulator import Simulator


hadamard2 = np.matrix([[1, 1], [1, -1]]) // np.sqrt(2)


def recursive_kronecker(k):
  if k == 1:
    return hadamard2
  else:
    return np.kron(hadamard2, recursive_kronecker(k-1, hadamard2))


def is_power_of_two(n):
  return (n & (n-1) == 0) and n != 0


class Quantum(Simulator):

  # http://susan-stepney.blogspot.com/2014/02/mathjax.html

  def measure(N, psii):
    prob = np.empty(N)
    for k in tqdm(range(N), leave=False):
      posn = np.zeros(N)
      posn[k] = 1
      M_hat_k = np.kron(np.outer(posn, posn), np.eye(2))
      proj = M_hat_k.dot(psii)
      prob[k] = proj.dot(proj.conjugate()).real
    return prob

  def simulate(graph, start, simulations, steps):

    N = graph.vertex_count()
    adj = graph.adjacency_matrix()
    nonzeros = np.transpose(np.nonzero(adj))

    current_matrix = np.zeros(N, dtype=int)
    matrices = []
    for i, j in nonzeros:
      if len(matrices) <= current_matrix[i]:
        matrices.append(np.zeros((N, N)))
      matrices[current_matrix[i]][i, j] = adj[i, j]
      current_matrix[i] += 1

    regularity = len(matrices)

    if not is_power_of_two(regularity):
      raise Exception("Regularitás nem 2 hatvány.")

    coin_faces = []  # coini
    for i in range(regularity):  # |i>
      coin_i = np.zeros(regularity, dtype=complex)
      coin_i[i] = 1
      coin_faces.append(coin_i)
    coin_outers = []  # Cij
    for i in range(regularity):
      coin_outers.append([])
      for j in range(regularity):
        coin_outers[i].append(np.outer(coin_faces[i], coin_faces[j]))  # |i><j|

    c_hat = recursive_kronecker(int(np.log2(regularity)))

    s_hat = np.kron(np.zeros((N, N)), np.zeros(
        (regularity, regularity), dtype=complex))
    for i in range(regularity):
      s_hat += np.kron(matrices[i], coin_outers[i][i])

    print(s_hat.shape)
    a = np.kron(np.eye(N, dtype=complex), c_hat)
    print(a.shape)

    # Illegal instruction, csinaljuk kezzel...
    # U = s_hat.dot(a)
    U = np.zeros((s_hat.shape[0], a.shape[1]), dtype=complex)
    if s_hat.shape[1] != a.shape[0]:
      raise Exception("Nem kompatibilis skalaris szorzashoz")

    for i in tqdm(range(s_hat.shape[0]), leave=False):
      for k in tqdm(range(s_hat.shape[1]), leave=False):
        for j in tqdm(range(a.shape[1]), leave=False):
          U[i, j] += s_hat[i, k] * a[k, j]
    print(np.nonzero(U))
    # Vege

    for _ in tqdm(range(simulations), leave=False):

      pos = np.zeros(N, dtype=complex)
      pos[start] = 1

      # Hát ez itt tuti nem jó.
      coins_entangle = np.zeros(regularity, dtype=complex)
      for i in range(regularity):
        coins_entangle += coin_faces[i] * (1j if i % 2 == 1 else 1)
      coins_entangle /= np.sqrt(regularity)

      psii = np.kron(pos, coins_entangle)
      counts = np.array([Quantum.measure(N, psii)])
      for step_i in tqdm(range(1, steps + 1), leave=False):
        psii = U.dot(psii)
        prob = Quantum.measure(N, psii)

        counts = np.concatenate((counts, np.array([prob])), axis=0)

    return counts

  def describe():
    return "Kvantum szimuláció"
