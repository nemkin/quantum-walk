from commands.files.archive import archive
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
      Quantum(Dft(), N//2, 1, 1000),
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
      Quantum(Dft(), 0, 1, 10),
  ]
  run = Run(graph, simulators)
  Exporter(run).export()
  Tester(run).test()


def run_path():
  graph = Graph('Path', [Path(range(16))])
  N = graph.vertex_count()
  simulators = [
      Classical(N//2, 10, 7),
      Quantum(Hadamard(), N//2, 1, 100),
      Quantum(Grover(), N//2, 1, 100),
      Quantum(Dft(), N//2, 1, 100)
  ]
  run = Run(graph, simulators)
  Exporter(run).export()
  Tester(run).test()


def run_grid():
  graph = Graph('Grid', [Grid(range(16))])
  N = graph.vertex_count()
  simulators = [
      Classical(N//2, 50, 100),
      Quantum(Hadamard(), N//2, 1, 100),
      Quantum(Grover(), N//2, 1, 100),
      Quantum(Dft(), N//2, 1, 100),
  ]
  run = Run(graph, simulators)
  Exporter(run).export()
  Tester(run).test()


def run_hypercube():
  graph = Graph('Hypercube', [Hypercube(range(2**4))])
  simulators = [
      Classical(0, 1000, 1000),
      Quantum(Hadamard(), 0, 1, 100),
      Quantum(Grover(), 0, 1, 100),
      Quantum(Dft(), 0, 1, 100),
  ]
  run = Run(graph, simulators)
  Exporter(run).export()
  Tester(run).test()


archive()
# run_dumbbell()
# run_glued_binary()
run_path()
run_grid()
run_hypercube()


# def is_unitary(m):
#   return np.allclose(np.eye(m.shape[0]), m.dot(m.T.conj()))
