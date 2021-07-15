class Simulator(object):

  def __init__(self, start, simulations, steps):
    self.start = start
    self.simulations = simulations
    self.steps = steps

  def is_quantum(self):
    return False
