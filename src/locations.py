import os
from pathlib import Path
from config import Config


class Locations:
  def indexed(file, index):
    return f"{file}_{index:02}"

  def makedirs(self, path):
    if not self.latex:
      try:
        os.makedirs(path.parents[0])
      except OSError:
        pass
    return path


class FileEnding(Locations):
  def __init__(self, path, latex):
    self.path = path
    self.latex = latex

  def image(self):
    return self.makedirs(self.path.with_suffix(".jpg"))

  def numpy(self):
    return self.makedirs(self.path.with_suffix(".npy"))

  def text(self):
    return self.makedirs(self.path.with_suffix(".txt"))


class SimulationLocations(Locations):
  def __init__(self, root, index, latex):
    self.root = root / Locations.indexed("sim", index)
    self.index = index
    self.latex = latex

  def counts(self):
    return FileEnding(self.root / "counts", self.latex)

  def counts_short(self):
    return FileEnding(self.root / "counts_short", self.latex)

  def hitting_time(self):
    return FileEnding(self.root / "hitting_time", self.latex)

  def mixing_time(self):
    return FileEnding(self.root / "mixing_time", self.latex)


class RunLocations(Locations):
  def __init__(self, run):
    self.run = run
    self.root = Config.new_root / self.run.filename
    self.latex = False
    self.makedirs(self.root)

  def get_root(self, latex):
    return self.root if not latex else Path('.')

  def graph_adj(self, latex=False):
    return FileEnding(self.get_root(latex) / "graph" / "graph", latex)

  def subgraph_adj(self, index, latex=False):
    return FileEnding(self.get_root(latex) / "graph" / Locations.indexed("sub_graph", index), latex)

  def coin_face(self, index, latex=False):
    return FileEnding(self.get_root(latex) / "coin_faces" / Locations.indexed("coin_face", index), latex)

  def simulation(self, index, latex=False):
    return SimulationLocations(self.get_root(latex), index, latex)
