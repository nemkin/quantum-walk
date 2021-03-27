import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

from graphs.Graph import Graph
from graphs.subgraphs.Circle import Circle
from graphs.subgraphs.BinaryTree import BinaryTree
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


graph = Graph()
sub_graph = BinaryTree(range(1000)) #, list(range(-10,10+1)))
graph.sub_graphs.append(sub_graph)

N = graph.vertex_count()
simulations = 1000
steps = 1000
counts = simulate_classical(graph, N//2, simulations, steps)
draw(N, steps, counts, "../generations/new/cucc.jpg")
