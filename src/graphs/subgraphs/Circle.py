from graphs.subgraphs.SubGraph import SubGraph


class Circle(SubGraph):

  def __init__(self, vertexes, neighbour_distances):
    self.vertexes = list(vertexes)
    self.neighbour_distances = neighbour_distances

  def neighbours(self, vertex):
    try:
      index = self.vertexes.index(vertex)
    except ValueError:
      return []

    return list(map(lambda dist: self.vertexes[(dist + index) % len(self.vertexes)], self.neighbour_distances))

  def describe(self):
    dist_str = ", ".join(map(str, self.neighbour_distances))
    return f"Kör {dist_str} távolságokat behúzva"
