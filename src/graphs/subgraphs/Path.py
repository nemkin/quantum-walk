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

    return list(map(lambda i: self.vertexes[i], filter(lambda i: 0 <= i < n, [0 if index == 0 else index-1, n-1 if index == (n-1) else index+1])))

  def describe(self):
    return f"Irányítatlan élekből álló út."
