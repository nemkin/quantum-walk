import os
from pathlib import Path
from config import Config


class Locations:
  def indexed(file, index):
    return f"{file}_{index:02}"

  def makedirs(self, path):
    if not self.is_latex:
      try:
        os.makedirs(path.parents[0])
      except OSError:
        pass
    return path


class FileEnding(Locations):
  def __init__(self, path, is_latex):
    self.path = path
    self.is_latex = is_latex

  def image(self):
    return self.makedirs(self.path.with_suffix(".jpg"))

  def numpy(self):
    return self.makedirs(self.path.with_suffix(".npy"))

  def text(self):
    return self.makedirs(self.path.with_suffix(".txt"))

  def latex(self):
    return self.makedirs(self.path.with_suffix(".tex"))


class SimulationLocations(Locations):
  def __init__(self, root, index, is_latex):
    self.root = root / Locations.indexed("sim", index)
    self.index = index
    self.is_latex = is_latex

  def counts(self):
    return FileEnding(self.root / "counts", self.is_latex)

  def counts_short(self):
    return FileEnding(self.root / "counts_short", self.is_latex)

  def hitting_time(self):
    return FileEnding(self.root / "hitting_time", self.is_latex)

  def mixing_time(self):
    return FileEnding(self.root / "mixing_time", self.is_latex)

  def coin_start(self):
    return FileEnding(self.root / "coin_start", self.is_latex)

  def coin_step(self):
    return FileEnding(self.root / "coin_step", self.is_latex)

  def simulation_matrix(self):
    return FileEnding(self.root / "simulation_matrix", self.is_latex)


class RunLocations(Locations):
  def __init__(self, run):
    self.run = run
    self.root = Config.new_root / self.run.filename
    self.is_latex = False
    self.makedirs(self.root)

  def get_root(self, is_latex):
    return self.root if not is_latex else Path('.')

  def graph_adj(self, is_latex=False):
    return FileEnding(self.get_root(is_latex) / "graph" / "graph", is_latex)

  def subgraph_adj(self, index, is_latex=False):
    return FileEnding(self.get_root(is_latex) / "graph" / Locations.indexed("sub_graph", index), is_latex)

  def coin_face(self, index, is_latex=False):
    return FileEnding(self.get_root(is_latex) / "coin_faces" / Locations.indexed("coin_face", index), is_latex)

  def simulation(self, index, is_latex=False):
    return SimulationLocations(self.get_root(is_latex), index, is_latex)
