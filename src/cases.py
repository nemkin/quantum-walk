import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

from graphs.Graph import Graph
from graphs.subgraphs.Circle import Circle
from graphs.subgraphs.BinaryTree import BinaryTree
from graphs.subgraphs.Bipartite import Bipartite
from graphs.subgraphs.Random import Random
from simulators.classical import simulate_classical


def draw_adj(adj, filename):
  fig, ax = plt.subplots(1, 1, figsize=(6, 6))
  X, Y = np.meshgrid(range(adj.shape[0]+1), range(adj.shape[1]+1))
  ax.pcolormesh(
      X,
      Y,
      adj,
      cmap='plasma',
      shading='auto',
      linewidths=1,
      snap=True,
      norm=colors.LogNorm(1, vmax=adj.max())
  )
  fig.tight_layout()
  fig.savefig(filename)
  plt.close(fig)


def draw(N, steps, counts, filename):

  steps_Y = np.arange(-0.5, steps, 1)
  vertexes_X = np.arange(-0.5, N-1, 1)

  fig, ax = plt.subplots(1, 1)
  pcm = ax.pcolor(
      vertexes_X,
      steps_Y,
      counts,
      cmap='plasma',
      shading='auto',
      linewidths=1,
      snap=True,
      norm=colors.LogNorm(1, vmax=counts.max())
  )
  ax.set_xlabel('Csúcsindexek')
  ax.set_ylabel('Lépések')
  fig.tight_layout()
  fig.savefig(filename)
  plt.close(fig)


def run_dumbbell():
  graph = Graph()

  graph.sub_graphs.append(Circle(range(0,   100), range(-4, 4+1)))
  graph.sub_graphs.append(Circle(range(100, 200), range(-4, 4+1)))
  graph.sub_graphs.append(Bipartite(range(0, 10), range(100, 110)))

  N = graph.vertex_count()
  simulations = 1000
  steps = 1000
  counts = simulate_classical(graph, N//2, simulations, steps)
  draw(N, steps, counts, "../generations/new/cucc.jpg")


def run_glued_binary():
  graph = Graph()

  size = 2**5

  graph.sub_graphs.append(BinaryTree(range(0, size-1)))
  graph.sub_graphs.append(BinaryTree(range(size-1, size-1 + size-1)))
  graph.sub_graphs.append(
      Bipartite(range(size//2, size-1), range(size-1 + size//2, size-1 + size-1)))

  draw_adj(graph.adjacency_matrix(), '../generations/new/cucc_1.jpg')
  N = graph.vertex_count()
  draw_adj(graph.sub_graphs[0].adjacency_matrix(N),
           '../generations/new/cucc_2.jpg')
  draw_adj(graph.sub_graphs[1].adjacency_matrix(N),
           '../generations/new/cucc_3.jpg')
  draw_adj(graph.sub_graphs[2].adjacency_matrix(N),
           '../generations/new/cucc_4.jpg')

  N = graph.vertex_count()
  simulations = 1000
  steps = 1000
  counts = simulate_classical(graph, N//2, simulations, steps)
  draw(N, steps, counts, "../generations/new/cucc.jpg")


run_glued_binary()
