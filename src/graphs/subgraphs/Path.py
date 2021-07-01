from graphs.subgraphs.SubGraph import SubGraph


class Path(SubGraph):

  def __init__(self, vertexes):
    self.vertexes = list(vertexes)

  def neighbours(self, vertex):
    try:
      index = self.vertexes.index(vertex)
    except ValueError:
      return []

    n = len(self.vertexes)

    return list(map(lambda i: self.vertexes[i], filter(lambda i: 0 <= i < n, [(index-1) % n, (index+1) % n])))

  def describe(self):
    return f"Irányítatlan élekből álló út."
