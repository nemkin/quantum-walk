from tqdm import tqdm
import pydng
import time


class Run:

  def make_name(self):
    time_part = time.strftime('%Y_%m_%d__%H_%M_%S')
    unique_part = pydng.generate_name()
    return f"{time_part}_{unique_part}"

  def __init__(self, graph, simulators):
    self.name = self.make_name()
    self.N = graph.vertex_count()
    self.graph_adj = graph.adjacency_matrix()
    self.coin_faces = graph.coin_faces()
    self.sub_graphs = map(
        lambda sub_graph: {
            "describe": sub_graph.describe(),
            "adj": sub_graph.adjacency_matrix(self.N)
        },
        tqdm(graph.sub_graphs, leave=False)
    )
    self.simulations = map(
        lambda s: {"simulator": s, "counts": s.simulate(graph)}, tqdm(simulators, leave=False))
