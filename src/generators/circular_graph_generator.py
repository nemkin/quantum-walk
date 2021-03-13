import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from scipy.sparse import rand
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize


def generate(N, distances, density):
    identity = np.array(range(N))
    shifted = (identity + 1) % N
    ones = np.array([1]*N)

    # Initialise loopbacks
    graph = csr_matrix((ones, (identity, identity)), shape=(N, N))

    # Next neighbour connections forwards and backwards
    perm_fwd = csr_matrix((ones, (identity, shifted)), shape=(N, N))
    perm_bck = csr_matrix((ones, (shifted, identity)), shape=(N, N))

    add_fwd = perm_fwd
    add_bck = perm_bck

    for i in range(1, max(distances)+1):

        if i in distances:
            graph += add_fwd
            graph += add_bck

        add_fwd *= perm_fwd
        add_bck *= perm_bck

    rand_edges = rand(N, N, density=density, format='csr')

    graph += rand_edges
    graph.data[:] = 1

    graph = normalize(graph, norm='l1')
    return graph


def draw_graph(graph, ax):
    nx_graph = nx.from_scipy_sparse_matrix(graph)
    pos = nx.circular_layout(nx_graph)
    nx.draw_networkx(nx_graph, pos=pos, with_labels=True, ax=ax)
