import progressbar
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from generate_graph import generate


def move(pos, N, graph):
    pos = np.random.choice(N, 1, p=graph[pos, :].todense().flat)
    return pos


def simulate(N, simulations, steps, w, density, filename):

    graph = generate(N, range(1, w+1), density)
    start = N // 2

    print(
        f'N={N}, '
        f'w={w}, '
        f'density={density}, '
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

    steps_Y = np.arange(-0.5, steps, 1)
    vertexes_X = np.arange(-0.5, N-1, 1)

    fig, ax = plt.subplots(1, 1, figsize=(6, 9))
    pcm = ax.pcolormesh(
        vertexes_X,
        steps_Y,
        counts,
        cmap='plasma',
        shading='auto',
        norm=colors.LogNorm(vmin=counts.min(), vmax=counts.max())
    )
    ax.set_title(
        f'Csúcsok száma: {N}\n'
        f'Szélesség: {w}\n'
        f'Véletlen élek: {density}\n'
        f'Kiindulási csúcs: {start}\n'
        f'Futások darabszáma: {simulations}\n'
        f'Lépések száma egy futásban: {steps}',
        loc='left'
    )
    ax.set_xlabel('Csúcsindexek')
    ax.set_ylabel('Lépések')
    fig.colorbar(pcm, ax=ax, extend='max')

    fig.savefig(
        f'{filename}.png',
        dpi=600,
        bbox_inches='tight'
    )
    plt.close(fig)
