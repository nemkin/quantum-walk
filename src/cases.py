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

from commands import run
from commands import archive


def run_dumbbell():
  print('Dumbbell:')
  graph = Dumbbell(100, 2, 10)
  N = graph.vertex_count()
  sim_configs = [
      [Classical, N//2, 1, 1000],
      [Classical, N//2, 10, 1000],
      [Classical, N//2, 100, 1000],
      [Classical, N//2, 1000, 1000],
      [Quantum, N//2, 1, 1000],
  ]
  run(graph, sim_configs)


def run_glued_binary():
  print('Glued binary:')
  graph = GluedBinary(10)
  sim_configs = [
      [Classical, 0, 1, 1000],
      [Classical, 0, 10, 1000],
      [Classical, 0, 100, 1000],
      [Classical, 0, 1000, 1000],
      [Quantum, 0, 1, 10],
  ]
  run(graph, sim_configs)


def run_path():
  print('Path:')
  graph = Graph([Path(range(5))])
  N = graph.vertex_count()
  sim_configs = [
      # [Classical, N//2, 50000, 100],
      [Quantum, N//2, 1, 10]
  ]
  run(graph, sim_configs)


def run_grid():
  print('Grid:')
  graph = Graph([Grid(range(100))])
  N = graph.vertex_count()
  sim_configs = [
      # [Classical, N//2, 1, 1000],
      # [Classical, N//2, 10, 1000],
      # [Classical, N//2, 100, 1000],
      # [Classical, N//2, 1000, 1000],
      [Quantum, N//2, 1, 1000],
  ]
  run(graph, sim_configs)


archive()
# run_dumbbell()
# run_glued_binary()
run_path()
# run_grid()
