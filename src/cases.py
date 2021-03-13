from datetime import datetime
from simulators.classical_simulator import simulate, draw_simulation
from generators.circular_graph_generator import draw_graph, generate
import matplotlib.pyplot as plt
root_path = "../generations/new"


def now():
    return datetime.now().strftime("%Y_%m_%d__%H_%M_%S")


def run_case(vertex_count, walker_count, step_count, distance, density, filename):
    fig, ax = plt.subplots(1, 2, figsize=(30, 15))
    graph = generate(vertex_count, range(1, distance+1), density)
    draw_graph(graph, ax[0])
    start = vertex_count // 2
    counts = simulate(graph, start, walker_count, step_count)
    draw_simulation(vertex_count, step_count, counts, ax[1])
    fig.savefig(
        f'{filename}.png',
        dpi=300,
        bbox_inches='tight'
    )
    plt.close(fig)


run_case(51, 1, 1000, 1, 0, f'{root_path}/{now()}_counts_circle')
run_case(51, 1, 1000, 2, 0, f'{root_path}/{now()}_counts_circle')
run_case(51, 1, 1000, 3, 0, f'{root_path}/{now()}_counts_circle')
run_case(51, 1, 1000, 3, 0.002, f'{root_path}/{now()}_counts_circle')

run_case(51, 10, 1000, 1, 0, f'{root_path}/{now()}_counts_circle')
run_case(51, 10, 1000, 2, 0, f'{root_path}/{now()}_counts_circle')
run_case(51, 10, 1000, 3, 0, f'{root_path}/{now()}_counts_circle')
run_case(51, 10, 1000, 3, 0.002, f'{root_path}/{now()}_counts_circle')

run_case(51, 1000, 1000, 1, 0, f'{root_path}/{now()}_counts_circle')
run_case(51, 1000, 1000, 2, 0, f'{root_path}/{now()}_counts_circle')
run_case(51, 1000, 1000, 3, 0, f'{root_path}/{now()}_counts_circle')
run_case(51, 1000, 1000, 3, 0.002, f'{root_path}/{now()}_counts_circle')
