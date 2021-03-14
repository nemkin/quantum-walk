from datetime import datetime
from simulators.classical import simulate_classical, draw_classical
from generators.circular_graph import generate_circular_graph
from generators.dumbbell_graph import generate_dumbbell_graph
import matplotlib.pyplot as plt
from pathlib import Path
import sys

new = Path("../generations/new")
archives = Path("../generations/archives")
new.mkdir(parents=True, exist_ok=True)
archives.mkdir(parents=True, exist_ok=True)

for src_file in new.glob('*.*'):
    src_file.rename(archives / src_file.parts[-1])


def now():
    return datetime.now().strftime("%Y_%m_%d__%H_%M_%S")


def setup_plots(vertex_count, step_count):
    fig, ax = plt.subplots(2, 1, figsize=(6, 20), dpi=150,
                           gridspec_kw={'height_ratios': [6, 14], 'hspace': 0})
    fig.tight_layout()
    return fig, ax


def run_circular_classical_case(vertex_count, walker_count, step_count, connection_distances, density):
    filename = f'{new}/{now()}_circular_classical.jpg'
    fig, ax = setup_plots(vertex_count, step_count)
    graph = generate_circular_graph(
        vertex_count, connection_distances, density)
    ax[0].spy(graph)
    start = vertex_count // 2
    counts = simulate_classical(graph, start, walker_count, step_count)
    draw_classical(vertex_count, step_count, counts, ax[1])
    # plt.show()
    fig.savefig(filename, bbox_inches='tight')
    plt.close(fig)


def run_dumbbell_classical_case(vertex_count, walker_count, step_count, connection_distances, density):
    filename = f'{new}/{now()}_dumbbell_classical.jpg'
    fig, ax = setup_plots(vertex_count, step_count)
    graph = generate_dumbbell_graph(
        vertex_count, connection_distances, density)
    ax[0].spy(graph)
    start = vertex_count // 2
    counts = simulate_classical(graph, start, walker_count, step_count)
    draw_classical(vertex_count, step_count, counts, ax[1])
    fig.savefig(filename, bbox_inches='tight')
    plt.close(fig)


run_circular_classical_case(51, 1, 1000, [1], 0)
run_dumbbell_classical_case(50, 1, 1000, [1, 2], 0)
sys.exit()

run_circular_classical_case(51, 1, 1000, [1, 2], 0)
run_circular_classical_case(51, 1, 1000, [1, 2, 3], 0)
run_circular_classical_case(51, 1, 1000, [1, 2, 3], 0.002)

run_circular_classical_case(51, 10, 1000, [1], 0)
run_circular_classical_case(51, 10, 1000, [1, 2], 0)
run_circular_classical_case(51, 10, 1000, [1, 2, 3], 0)
run_circular_classical_case(51, 10, 1000, [1, 2, 3], 0.002)

run_circular_classical_case(51, 1000, 1000, [1], 0)
run_circular_classical_case(51, 1000, 1000, [1, 2], 0)
run_circular_classical_case(51, 1000, 1000, [1, 2, 3], 0)
run_circular_classical_case(51, 1000, 1000, [1, 2, 3], 0.002)
