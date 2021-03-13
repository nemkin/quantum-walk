from datetime import datetime
from simulators.classical import simulate_classical, draw_classical
from generators.circular_graph import generate_circular_graph, draw_circular_graph
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams.update({'font.size': 50})

new = Path("../generations/new")
archives = Path("../generations/archives")
new.mkdir(parents=True, exist_ok=True)
archives.mkdir(parents=True, exist_ok=True)

for src_file in new.glob('*.*'):
    src_file.rename(archives / src_file.parts[-1])


def now():
    return datetime.now().strftime("%Y_%m_%d__%H_%M_%S")


def run_circular_classical_case(vertex_count, walker_count, step_count, connection_distances, density):
    filename = f'{new}/{now()}_circular_classical.jpg'
    fig, ax = plt.subplots(1, 2, figsize=(
        60, 45), gridspec_kw={'width_ratios': [3, 1]})
    graph = generate_circular_graph(
        vertex_count, connection_distances, density)
    draw_circular_graph(graph, ax[0])
    start = vertex_count // 2
    counts = simulate_classical(graph, start, walker_count, step_count)
    draw_classical(vertex_count, step_count, counts, ax[1])
    fig.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close(fig)


run_circular_classical_case(51, 1, 1000, [1], 0, )
run_circular_classical_case(51, 1, 1000, [1, 2], 0,)
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
