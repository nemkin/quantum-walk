import numpy as np
import networkx as nx
from scipy.sparse import rand
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize


def generate_circular_graph(vertex_count, connection_distances, randomness):
    identity = np.array(range(vertex_count))
    shifted = (identity + 1) % vertex_count
    ones = np.array([1]*vertex_count)

    # Initialise loopbacks
    graph = csr_matrix((ones, (identity, identity)),
                       shape=(vertex_count, vertex_count))

    # Next neighbour connections forwards and backwards
    perm_fwd = csr_matrix((ones, (identity, shifted)),
                          shape=(vertex_count, vertex_count))
    perm_bck = csr_matrix((ones, (shifted, identity)),
                          shape=(vertex_count, vertex_count))

    add_fwd = perm_fwd
    add_bck = perm_bck

    for i in range(1, max(connection_distances)+1):

        if i in connection_distances:
            graph += add_fwd
            graph += add_bck

        add_fwd *= perm_fwd
        add_bck *= perm_bck

    rand_edges = rand(vertex_count, vertex_count,
                      density=randomness, format='csr')

    graph += rand_edges
    graph.data[:] = 1

    graph = normalize(graph, norm='l1')
    return graph


def draw_circular_graph(graph, ax):
    nx_graph = nx.from_scipy_sparse_matrix(graph)
    pos = nx.circular_layout(nx_graph)
    nx.draw_networkx(nx_graph, pos=pos, with_labels=True, ax=ax)
