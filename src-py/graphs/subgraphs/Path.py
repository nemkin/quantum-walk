from graphs.subgraphs.SubGraph import SubGraph


class Path(SubGraph):

  def __init__(self, vertexes):
    self.vertexes = list(vertexes)
    self.n = len(self.vertexes)

  def left(self, index):
    if index % 2:
      return max(0, index-1)
    else:
      return min(self.n-1, index+1)

  def right(self, index):
    if index % 2:
      return min(self.n-1, index+1)
    else:
      return max(0, index-1)

  def neighbours(self, vertex):
    try:
      index = self.vertexes.index(vertex)
    except ValueError:
      return []

    n = len(self.vertexes)

    return list(map(lambda i: self.vertexes[i], [self.left(index), self.right(index)]))

  def describe(self):
    return f"Iranyitatlan elekbol allo ut."
