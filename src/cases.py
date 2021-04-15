from graphs.Graph import Graph
from graphs.composites.Dumbbell import Dumbbell
from graphs.composites.GluedBinary import GluedBinary
from graphs.subgraphs.Circle import Circle
from graphs.subgraphs.BinaryTree import BinaryTree
from graphs.subgraphs.Bipartite import Bipartite
from graphs.subgraphs.Path import Path
from graphs.subgraphs.Random import Random
from simulators.classical import Classical

from commands import run
from commands import archive


def run_dumbbell():
  graph = Dumbbell(100, 2, 10)
  N = graph.vertex_count()
  sim_configs = [
      [Classical, N//2, 1, 1000],
      [Classical, N//2, 10, 1000],
      [Classical, N//2, 100, 1000],
      [Classical, N//2, 1000, 1000]
  ]
  run(graph, sim_configs)


def run_glued_binary():
  graph = GluedBinary(5)
  sim_configs = [
      [Classical, 0, 1, 1000],
      [Classical, 0, 10, 1000],
      [Classical, 0, 100, 1000],
      [Classical, 0, 1000, 1000]
  ]
  run(graph, sim_configs)


def run_path():
  graph = Graph(Path(range(100)))
  N = graph.vertex_count()
  sim_configs = [
      [Classical, N//2, 1, 1000],
      [Classical, N//2, 10, 1000],
      [Classical, N//2, 100, 1000],
      [Classical, N//2, 1000, 1000]
  ]
  run(graph, sim_configs)


archive()
run_dumbbell()
run_glued_binary()
run_path()
