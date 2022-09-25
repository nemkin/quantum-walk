from graphs.subgraphs.SubGraph import SubGraph


class Path(SubGraph):

  def __init__(self, vertexes):
    self.vertexes = list(vertexes)
    self.n = len(self.vertexes)

  def left(self, index):
    return (index-1) % self.n
    # TODO: Nem permutáció mátrix!
    if 0 <= index-1:
      return index-1
    else:
      return index

  def right(self, index):
    return (index+1) % self.n
    # TODO: Nem permutáció mátrix!
    if index+1 < self.n:
      return index+1
    else:
      return index

  def neighbours(self, vertex):
    try:
      index = self.vertexes.index(vertex)
    except ValueError:
      return []

    n = len(self.vertexes)

    return list(map(lambda i: self.vertexes[i], [self.left(index), self.right(index)]))

  def describe(self):
    return f"Irányítatlan élekből álló út."
