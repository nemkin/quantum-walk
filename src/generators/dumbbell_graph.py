import numpy as np
import networkx as nx
from scipy.sparse import rand
from scipy.sparse import csr_matrix
from scipy.sparse.construct import hstack, vstack
from sklearn.preprocessing import normalize

from generators.circular_graph import generate_circular_graph


def generate_dumbbell_graph(vertex_count, connection_distances, randomness):
    if vertex_count % 2 != 0:
        raise Exception("Dumbbell graph must have even vertex count!")
    sides_count = vertex_count // 2

    top_left_corner = generate_circular_graph(
        sides_count, connection_distances, randomness)

    bottom_right_corner = generate_circular_graph(
        sides_count, connection_distances, randomness)

    top_right_corner = csr_matrix((sides_count, sides_count))
    top_right_corner[sides_count//2, sides_count//2] = 1

    bottom_left_corner = csr_matrix((sides_count, sides_count))

    print(top_left_corner, bottom_right_corner)

    top = hstack([top_left_corner, top_right_corner])
    bottom = hstack([bottom_left_corner, bottom_right_corner])
    graph = vstack([top, bottom])

    graph = normalize(graph, norm='l1')
    return graph


def draw_dumbbell_graph(graph, ax):
    nx_graph = nx.from_scipy_sparse_matrix(graph)
    nx.draw_networkx(nx_graph, with_labels=True, ax=ax)
