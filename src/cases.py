import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

from graphs.Graph import Graph
from graphs.subgraphs.Circle import Circle
from graphs.subgraphs.BinaryTree import BinaryTree
from graphs.subgraphs.Bipartite import Bipartite
from graphs.subgraphs.Random import Random
from simulators.classical import simulate_classical


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
        linewidths=1, snap=True,
        norm=colors.LogNorm(1, vmax=counts.max())
    )
    ax.set_xlabel('Csúcsindexek')
    ax.set_ylabel('Lépések')
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)


def run_dumbbell():
  graph = Graph()

  graph.sub_graphs.append(Circle(range(0,   100), range(-4,4+1)))
  graph.sub_graphs.append(Circle(range(100, 200), range(-4,4+1)))
  graph.sub_graphs.append(Bipartite(range(0, 10), range(100, 110)))

  N = graph.vertex_count()
  simulations = 1000
  steps = 1000
  counts = simulate_classical(graph, N//2, simulations, steps)
  draw(N, steps, counts, "../generations/new/cucc.jpg")

def run_glued_binary():
  graph = Graph()

  graph.sub_graphs.append(BinaryTree(range(0, 2**10-1)))
  graph.sub_graphs.append(BinaryTree(range(2**10-1, 2**10-1 + 2**10-1)))
  graph.sub_graphs.append(Bipartite(range(2**9, 2**10-1), range(2**10-1 + 2**9, 2**10-1 + 2**10-1)))

  N = graph.vertex_count()
  simulations = 1000
  steps = 1000
  counts = simulate_classical(graph, N//2, simulations, steps)
  draw(N, steps, counts, "../generations/new/cucc.jpg")

run_glued_binary()