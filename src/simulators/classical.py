import progressbar
import numpy as np
import matplotlib.colors as colors


def move(pos, N, graph):
    pos = np.random.choice(N, 1, p=graph[pos, :].todense().flat)
    return pos


def simulate_classical(graph, start, simulations, steps):

    N = graph.get_shape()[0]
    print(
        f'N={N}, '
        #f'w={w}, '
        #f'density={density}, '
        f'start={start}, '
        f'simulations={simulations}, '
        f'steps={steps}'
    )

    counts = np.zeros([steps+1, N])
    counts += 0.01
    for _ in progressbar.progressbar(range(simulations)):
        pos = start
        counts[0, pos] += 1
        for step_i in range(1, steps+1):
            pos = move(pos, N, graph)
            counts[step_i, pos] += 1

    return counts


def draw_classical(N, steps, counts, ax):

    steps_Y = np.arange(-0.5, steps, 1)
    vertexes_X = np.arange(-0.5, N-1, 1)

    pcm = ax.pcolor(
        vertexes_X,
        steps_Y,
        counts,
        cmap='plasma',
        shading='auto',
        linewidths=1, snap=True,
        norm=colors.LogNorm(vmin=counts.min(), vmax=counts.max())
    )
    ax.invert_yaxis()
    ax.set_xlabel('Csúcsindexek')
    ax.set_ylabel('Lépések')
    #ax.figure.colorbar(pcm, ax=ax, aspect=100, orientation="horizontal")
