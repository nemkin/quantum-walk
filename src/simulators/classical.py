import random

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import progressbar


def simulate_classical(graph, start, simulations, steps):
  counts = np.zeros([steps+1, graph.vertex_count()])
  for _ in progressbar.progressbar(range(simulations)):
    pos = start
    counts[0, pos] += 1
    for step_i in range(1, steps + 1):
      options = graph.neighbours(pos)
      pos = random.choice(options)
      counts[step_i, pos] += 1
  return counts
