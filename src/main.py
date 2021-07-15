
from simulators.coins.grover import Grover
from simulators.coins.hadamard import Hadamard
from exporter import Exporter
from tester import Tester
from run import Run
from graphs.subgraphs.Grid import Grid
from graphs.Graph import Graph
from graphs.composites.Dumbbell import Dumbbell
from graphs.composites.GluedBinary import GluedBinary
from graphs.subgraphs.Circle import Circle
from graphs.subgraphs.BinaryTree import BinaryTree
from graphs.subgraphs.Bipartite import Bipartite
from graphs.subgraphs.Path import Path
from graphs.subgraphs.Random import Random
from simulators.classical import Classical
from simulators.quantum import Quantum

from commands import archive


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
  graph = Graph('Path', [Path(range(225))])
  N = graph.vertex_count()
  simulators = [
      Classical(N//2, 1000, 1000),
      Quantum(Grover(), N//2, 1, 1000)
  ]
  run = Run(graph, simulators)
  Exporter(run).export()
  Tester(run).test()


def run_grid():
  graph = Graph('Grid', [Grid(range(225))])
  N = graph.vertex_count()
  simulators = [
      Classical(N//2, 1000, 1000),
      Quantum(Grover(), N//2, 1, 1000),
  ]
  run = Run(graph, simulators)
  Exporter(run).export()
  Tester(run).test()


archive()
# run_dumbbell()
# run_glued_binary()
run_path()
run_grid()
