from tqdm import tqdm
import pydng
import time
import numpy as np
from datetime import datetime
import itertools


class Run:

  def make_name():
    now = datetime.now()
    time_filename = now.strftime('%Y_%m_%d__%H_%M_%S')
    time_title = now.strftime('%Y. %m. %d. %H:%M:%S')

    name_filename = pydng.generate_name()
    name_title = ' '.join(map(
        lambda s: s.capitalize(),
        name_filename.split('_')
    ))

    title = name_title
    subtitle = time_title
    filename = f"{time_filename}_{name_filename}"

    return title, subtitle, filename

  def eigens(adj):
    eigen_values, eigen_vectors = np.linalg.eig(adj)
    eigens = [{"value": eigen_values[i], "vector": eigen_vectors[i]}
              for i in range(len(eigen_values))]
    return {key: list(map(lambda g: g["vector"], group))
            for key, group in itertools.groupby(eigens, lambda x: x["value"])}

  def limiting_dists(adj, is_quantum):
    if is_quantum:
        transition_mat = adj
    else:
        transition_mat = adj / adj.sum(0)
    eigen_values, eigen_vectors = np.linalg.eig(transition_mat)
    eigen_vectors_1 = eigen_vectors[:, np.isclose(eigen_values, 1)]
    return eigen_vectors_1

  def mixing_time(counts):
    n = len(counts)
    diffarray = np.zeros(n-1)
    for i in range(n-1):
      diffarray[i] = np.linalg.norm(counts[n-1]-counts[i])
    return diffarray

  def hitting_time(counts):
    # https://stackoverflow.com/a/47269413
    mask = (counts != 0)
    axis = 0
    invalid_value = -1
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_value)

  def get_classical_simulation_matrix(graph):
    adj = graph.adjacency_matrix()
    return adj / adj.sum(axis=0)

  def get_quantum_simulation_matrix(graph, coin):
    regularity = graph.max_degree()
    N = graph.vertex_count()
    coin.set_size(regularity)

    graph_coin_faces = graph.coin_faces()
    coin_matrix = coin.step()

    S_hat = np.zeros((N*regularity, N*regularity), dtype=complex)
    for i in range(regularity):
      m = np.zeros((regularity, regularity), dtype=complex)
      m[i, i] = 1
      S_i = np.kron(graph_coin_faces[i], m)
      S_hat += S_i

    C_hat = np.kron(np.eye(N), coin_matrix)
    U = np.matmul(S_hat, C_hat)
    return U

  def get_simulation_matrix(graph, simulator):
    if simulator.is_quantum():
      return Run.get_quantum_simulation_matrix(graph, simulator.coin)
    else:
      return Run.get_classical_simulation_matrix(graph)

  def get_simulation(graph, simulator):
    counts = simulator.simulate(graph)
    mixing_time = Run.mixing_time(counts)
    hitting_time = Run.hitting_time(counts)
    simulation_matrix = Run.get_simulation_matrix(graph, simulator)
    return {
        "simulator": simulator,
        "counts": counts,
        "mixing_time": mixing_time,
        "hitting_time": hitting_time,
        "simulation_matrix": simulation_matrix,
        "eigens": Run.eigens(simulation_matrix),
        "limiting_dists": Run.limiting_dists(simulation_matrix, simulator.is_quantum())
    }

  def __init__(self, graph, simulators):
    self.title, self.subtitle, self.filename = Run.make_name()
    self.N = graph.vertex_count()
    self.graph_adj = graph.adjacency_matrix()
    self.coin_faces = graph.coin_faces()
    self.sub_graphs = map(
        lambda sub_graph: {
            "describe": sub_graph.describe(),
            "adj": sub_graph.adjacency_matrix(self.N)
        },
        tqdm(graph.sub_graphs,
             desc=f"{graph.name} subgraph adjacency matrices", leave=False)
    )
    self.simulations = map(
        lambda s: Run.get_simulation(graph, s),
        tqdm(simulators, desc=f"{graph.name} simulations",
             leave=False)
    )
