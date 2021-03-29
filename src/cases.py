import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import pydng
import time
import os
import shutil

from graphs.Graph import Graph
from graphs.subgraphs.Circle import Circle
from graphs.subgraphs.BinaryTree import BinaryTree
from graphs.subgraphs.Bipartite import Bipartite
from graphs.subgraphs.Random import Random
from simulators.classical import simulate_classical

new_root = "../generations/new"
archive_root = "../generations/archives"


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

  x = 6
  y = min(6*steps//N, 12)

  fig, ax = plt.subplots(1, 1, figsize=(x, y))
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


def archive():
  try:
    os.makedirs(new_root)
  except:
    pass
  try:
    os.makedirs(archive_root)
  except:
    pass
  file_names = os.listdir(new_root)
  for file_name in file_names:
    shutil.move(os.path.join(new_root, file_name), archive_root)


def make_name():
  time_part = time.strftime('%Y_%m_%d__%H_%M_%S')
  unique_part = pydng.generate_name()
  return f"{time_part}_{unique_part}"


def run(graph, sim_configs):
  name = make_name()
  dir = f"{new_root}/{name}"
  os.makedirs(dir)

  description = []
  description += ["\section{Gráf}"]

  graph_file = f'{dir}/graph.jpg'
  description += [f"Fotó: {graph_file}"]
  draw_adj(graph.adjacency_matrix(), graph_file)
  N = graph.vertex_count()

  for i in range(len(graph.sub_graphs)):
    description += ["\subsection{Részgráf}"]
    description += [graph.sub_graphs[i].describe()]
    sub_graph_file = f'{dir}/subgraph_{i:02}.jpg'
    description += [f"Fotó: {sub_graph_file}"]
    draw_adj(graph.sub_graphs[i].adjacency_matrix(N), sub_graph_file)

  description += ["\section{Szimulációk}"]
  N = graph.vertex_count()
  start = N//2

  for i in range(len(sim_configs)):
    description += ["\subsection{Szimuláció}"]
    simulations, steps = sim_configs[i]
    description += [f"Kezdőcsúcs: {start}"]
    description += [f"Bolyongók: {simulations}"]
    description += [f"Lépésszám: {steps}"]
    sim_file = f'{dir}/sim{i:02}.jpg'
    description += [f"Fotó: {sim_file}"]
    counts = simulate_classical(graph, start, simulations, steps)
    draw(N, steps, counts, sim_file)

  latex_file = f'{dir}/latex.tex'
  with open(latex_file, 'w') as f:
    f.writelines("\n".join(description))


def run_dumbbell():
  graph = Graph()
  graph.sub_graphs.append(Circle(range(0,   100), range(-4, 4+1)))
  graph.sub_graphs.append(Circle(range(100, 200), range(-4, 4+1)))
  graph.sub_graphs.append(Bipartite(range(0, 10), range(100, 110)))

  sim_configs = [[1000, 1000]]

  run(graph, sim_configs)


def run_glued_binary():
  graph = Graph()
  size = 2**5
  graph.sub_graphs.append(BinaryTree(range(0, size-1)))
  graph.sub_graphs.append(BinaryTree(range(size-1, size-1 + size-1)))
  graph.sub_graphs.append(
      Bipartite(range(size//2, size-1), range(size-1 + size//2, size-1 + size-1)))

  sim_configs = [[1000, 1000]]

  run(graph, sim_configs)


archive()
run_dumbbell()
run_glued_binary()
