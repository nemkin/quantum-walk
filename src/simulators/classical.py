import random

import numpy as np
import progressbar
from tqdm import tqdm

from simulators.simulator import Simulator


class Classical(Simulator):

  def simulate(graph, start, simulations, steps):
    counts = np.zeros([steps+1, graph.vertex_count()])
    for _ in tqdm(range(simulations), leave=False):
      pos = start
      counts[0, pos] += 1
      for step_i in tqdm(range(1, steps + 1), leave=False):
        options = graph.neighbours(pos)
        pos = random.choice(options)
        counts[step_i, pos] += 1
    return counts

  def describe():
    return "Klasszikus szimuláció"
