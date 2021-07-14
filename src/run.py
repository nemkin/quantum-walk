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

  def limiting_dists(adj):
    transition_mat = adj/adj.sum(0)
    eigen_values, eigen_vectors = np.linalg.eig(transition_mat)
    eigen_vectors_1 = eigen_vectors[:, np.isclose(eigen_values, 1)]
    return eigen_vectors_1

  def mixing_time(counts):
    n = len(counts)
    k = 2
    diffarray = np.zeros(n-k)
    for i in range(n-k):
      diffarray[i] = np.linalg.norm(counts[i+k]-counts[i])
    return diffarray

  def hitting_time(counts):
    # https://stackoverflow.com/a/47269413
    mask = (counts != 0)
    axis = 0
    invalid_value = -1
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_value)

  def get_simulation(graph, simulator):
    counts = simulator.simulate(graph)
    mixing_time = Run.mixing_time(counts)
    hitting_time = Run.hitting_time(counts)
    return {
        "simulator": simulator,
        "counts": counts,
        "mixing_time": mixing_time,
        "hitting_time": hitting_time
    }

  def __init__(self, graph, simulators):
    self.title, self.subtitle, self.filename = Run.make_name()
    self.N = graph.vertex_count()
    self.graph_adj = graph.adjacency_matrix()
    self.eigens = Run.eigens(self.graph_adj)
    self.limiting_dists = Run.limiting_dists(self.graph_adj)
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
