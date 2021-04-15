from graphs.subgraphs.SubGraph import SubGraph


class Path(SubGraph):
  vertexes = []

  def __init__(self, vertexes):
    self.vertexes = list(vertexes)

  def neighbours(self, vertex):
    try:
      index = self.vertexes.index(vertex)
    except ValueError:
      return []

    n = len(self.vertexes)
    return [max(index-1, 0), min(index+1, n-1)]

  def describe(self):
    return f"Irányítatlan élekből álló út, az első és az utolsó csúcson hurokéllel."
