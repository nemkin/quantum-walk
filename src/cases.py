from datetime import datetime
from simulate_circle_graph import simulate

root_path = "../generations/new"


def now():
    return datetime.now().strftime("%Y_%m_%d__%H_%M_%S")


# def run_case(vertex_count, walker_count, num_of_steps, w, density, filename):


simulate(101, 1, 1000, 1, 0, f'{root_path}/{now()}_counts_circle')
simulate(101, 1, 1000, 2, 0, f'{root_path}/{now()}_counts_circle')
simulate(101, 1, 1000, 3, 0, f'{root_path}/{now()}_counts_circle')
simulate(101, 1, 1000, 3, 0.2, f'{root_path}/{now()}_counts_circle')

simulate(101, 10, 1000, 1, 0, f'{root_path}/{now()}_counts_circle')
simulate(101, 10, 1000, 2, 0, f'{root_path}/{now()}_counts_circle')
simulate(101, 10, 1000, 3, 0, f'{root_path}/{now()}_counts_circle')
simulate(101, 10, 1000, 3, 0.2, f'{root_path}/{now()}_counts_circle')

simulate(101, 1000, 1000, 1, 0, f'{root_path}/{now()}_counts_circle')
simulate(101, 1000, 1000, 2, 0, f'{root_path}/{now()}_counts_circle')
simulate(101, 1000, 1000, 3, 0, f'{root_path}/{now()}_counts_circle')
simulate(101, 1000, 1000, 3, 0.2, f'{root_path}/{now()}_counts_circle')
