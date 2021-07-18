from commands import archive
from simulators.quantum import Quantum
from simulators.classical import Classical
from graphs.subgraphs.Random import Random
from graphs.subgraphs.Path import Path
from graphs.subgraphs.Bipartite import Bipartite
from graphs.subgraphs.BinaryTree import BinaryTree
from graphs.subgraphs.Circle import Circle
from graphs.composites.GluedBinary import GluedBinary
from graphs.composites.Dumbbell import Dumbbell
from graphs.Graph import Graph
from graphs.subgraphs.Grid import Grid
from run import Run
from tester import Tester
from exporter import Exporter
from simulators.coins.hadamard import Hadamard
from simulators.coins.grover import Grover
from graphs.subgraphs.Hypercube import Hypercube
from simulators.coins.dft import Dft
import numpy as np


def run_dumbbell():
  graph = Dumbbell(100, 2, 10)
  N = graph.vertex_count()
  simulators = [
      Classical(N//2, 1, 1000),
      Classical(N//2, 10, 1000),
      Classical(N//2, 100, 1000),
      Classical(N//2, 1000, 1000),
      Quantum(N//2, 1, 1000),
  ]

  run = Run(graph, simulators)
  Exporter(run).export()
  Tester(run).test()


def run_glued_binary():
  graph = GluedBinary(10)
  simulators = [
      Classical(0, 1, 1000),
      Classical(0, 10, 1000),
      Classical(0, 100, 1000),
      Classical(0, 1000, 1000),
      Quantum(0, 1, 10),
  ]
  run = Run(graph, simulators)
  Exporter(run).export()
  Tester(run).test()


def run_path():
  graph = Graph('Path', [Path(range(5))])
  N = graph.vertex_count()
  simulators = [
      # Classical(N//2, 10, 7),
      Quantum(Hadamard(), N//2, 1, 7)
  ]
  run = Run(graph, simulators)
  Exporter(run).export()
  Tester(run).test()


def run_grid():
  graph = Graph('Grid', [Grid(range(9))])
  N = graph.vertex_count()
  simulators = [
      Classical(N//2, 50, 50),
      Quantum(Grover(), N//2, 1, 50),
  ]
  run = Run(graph, simulators)
  Exporter(run).export()
  Tester(run).test()


def run_hypercube():
  graph = Graph('Hypercube', [Hypercube(range(2**8))])
  simulators = [
      Classical(0, 1000, 1000),
      Quantum(Hadamard(), 0, 1, 1000),
      # Quantum(Grover(), 0, 1, 1000),
      Quantum(Dft(), 0, 1, 1000),
  ]
  run = Run(graph, simulators)
  Exporter(run).export()
  Tester(run).test()


archive()
# run_dumbbell()
# run_glued_binary()

# run_path()
# run_grid()

# run_hypercube()


def is_unitary(m):
  return np.allclose(np.eye(m.shape[0]), m.dot(m.T.conj()))


coin = Hadamard()
graph = Graph('Path', [Path(range(5))])
regularity = graph.max_degree()
N = graph.vertex_count()
coin.set_size(regularity)

graph_coin_faces = graph.coin_faces()
coin_matrix = coin.step()

S_hat = np.zeros((N*regularity, N*regularity), dtype=complex)
for i in range(regularity):
  m = np.zeros((regularity, regularity), dtype=complex)
  m[:, i] = coin_matrix[:, i]
  S_hat += np.kron(graph_coin_faces[i], m)

print(np.array2string(S_hat, max_line_width=200, precision=2))
print(is_unitary(S_hat))

# current = np.identity(regularity*N, dtype=complex)
# for i in range(30):
#  current = S_hat.dot(current)
#  print()
#  print(np.array2string(current, max_line_width=200, precision=2))
