import random

import numpy as np
from tqdm import tqdm

from simulators.simulator import Simulator


class Classical(Simulator):

  def simulate(self, graph):
    counts = np.zeros([self.steps+1, graph.vertex_count()])
    for _ in tqdm(range(self.simulations), leave=False):
      pos = self.start
      counts[0, pos] += 1
      for step_i in tqdm(range(1, self.steps + 1), leave=False):
        options = graph.neighbours(pos)
        pos = random.choice(options)
        counts[step_i, pos] += 1
    return counts

  def describe(self):
    return "Klasszikus szimuláció"
