import numpy as np
from scipy.sparse import rand
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize

def generate(N, width, density):
  identity = np.array(range(N))
  shifted = (identity + 1) % N
  ones = np.array([1]*N)

  graph = csr_matrix((ones, (identity, identity)), shape=(N, N))

  perm_fwd = csr_matrix((ones, (identity, shifted)), shape=(N, N))
  perm_bck = csr_matrix((ones, (shifted, identity)), shape=(N, N))

  add_fwd = perm_fwd
  add_bck = perm_bck

  for _ in range(width):
    graph += add_fwd
    graph += add_bck

    add_fwd *= perm_fwd
    add_bck *= perm_bck

  rand_edges = rand(N, N, density=density, format='csr')

  graph += rand_edges
  graph.data[:] = 1

  graph = normalize(graph, norm='l1')
  return graph

if __name__ == '__main__':
  graph = generate(10,1,0.02)
  pos = np.random.choice(10, 1, p=graph[1,:].todense().flat)
  print(graph)
  print(pos)
