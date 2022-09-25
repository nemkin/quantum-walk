import random

import numpy as np
from tqdm import tqdm

from simulators.simulator import Simulator


class Classical(Simulator):

  def simulate(self, graph):
    N = graph.vertex_count()
    counts = np.zeros([self.steps+1, N])
    for _ in tqdm(range(self.simulations), desc=f"{graph.name}: {self.describe()} simulations", leave=False):
      pos = self.start
      counts[0, pos] += 1
      for step_i in tqdm(range(1, self.steps + 1), desc=f"{graph.name}: {self.describe()} steps", leave=False):
        options = graph.neighbours(pos)
        pos = random.choice(options)
        counts[step_i, pos] += 1
    return counts / self.simulations

  def describe(self):
    return "Classical simulation"
