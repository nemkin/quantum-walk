class Circle(object):
  vertexes = []
  neighbour_distances = []

  def __init__(self, vertexes, neighbour_distances):
    self.vertexes = list(vertexes)
    self.neighbour_distances = neighbour_distances

  def neighbours(self, vertex):
    try:
      index = self.vertexes.index(vertex)
    except ValueError:
      return [vertex]

    return list(map(lambda dist: self.vertexes[(dist + index) % len(self.vertexes)], self.neighbour_distances))
