
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
  print('Dumbbell:')
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
  Tester(run).test()
  Exporter(run).export()


def run_glued_binary():
  print('Glued binary:')
  graph = GluedBinary(10)
  simulators = [
      Classical(0, 1, 1000),
      Classical(0, 10, 1000),
      Classical(0, 100, 1000),
      Classical(0, 1000, 1000),
      Quantum(0, 1, 10),
  ]
  run = Run(graph, simulators)
  Tester(run).test()
  Exporter(run).export()


def run_path():
  print('Path:')
  graph = Graph([Path(range(10))])
  N = graph.vertex_count()
  simulators = [
      Classical(N//2, 50, 100),
      Quantum(N//2, 1, 100)
  ]
  run = Run(graph, simulators)
  Tester(run).test()
  Exporter(run).export()


def run_grid():
  print('Grid:')
  graph = Graph([Grid(range(16))])
  N = graph.vertex_count()
  simulators = [
      Classical(N//2, 1, 1000),
      Classical(N//2, 10, 1000),
      Classical(N//2, 100, 1000),
      Classical(N//2, 1000, 1000),
      Quantum(N//2, 1, 30),
      Quantum(N//2, 1, 100),
      Quantum(N//2, 1, 500),
      Quantum(N//2, 1, 1000),
  ]
  run = Run(graph, simulators)
  Tester(run).test()
  Exporter(run).export()


archive()
# run_dumbbell()
# run_glued_binary()
run_path()
# run_grid()
