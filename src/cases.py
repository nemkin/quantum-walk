from datetime import datetime
from simulators.classical_simulator import simulate, draw_simulation
from generators.circular_graph_generator import generate
root_path = "../generations/new"


def now():
    return datetime.now().strftime("%Y_%m_%d__%H_%M_%S")


def run_case(vertex_count, walker_count, step_count, distance, density, filename):
    graph = generate(vertex_count, range(1, distance+1), density)
    start = vertex_count // 2
    counts = simulate(graph, start, walker_count, step_count)
    draw_simulation(vertex_count, step_count, counts, filename)


run_case(101, 1, 1000, 1, 0, f'{root_path}/{now()}_counts_circle')
run_case(101, 1, 1000, 2, 0, f'{root_path}/{now()}_counts_circle')
run_case(101, 1, 1000, 3, 0, f'{root_path}/{now()}_counts_circle')
run_case(101, 1, 1000, 3, 0.2, f'{root_path}/{now()}_counts_circle')

run_case(101, 10, 1000, 1, 0, f'{root_path}/{now()}_counts_circle')
run_case(101, 10, 1000, 2, 0, f'{root_path}/{now()}_counts_circle')
run_case(101, 10, 1000, 3, 0, f'{root_path}/{now()}_counts_circle')
run_case(101, 10, 1000, 3, 0.2, f'{root_path}/{now()}_counts_circle')

run_case(101, 1000, 1000, 1, 0, f'{root_path}/{now()}_counts_circle')
run_case(101, 1000, 1000, 2, 0, f'{root_path}/{now()}_counts_circle')
run_case(101, 1000, 1000, 3, 0, f'{root_path}/{now()}_counts_circle')
run_case(101, 1000, 1000, 3, 0.2, f'{root_path}/{now()}_counts_circle')
