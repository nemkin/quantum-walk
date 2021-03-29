from graphs.subgraphs.SubGraph import SubGraph


class BinaryTree(SubGraph):
  vertexes = []

  def __init__(self, vertexes):
    self.vertexes = list(vertexes)

  def neighbours(self, vertex):
    try:
      index = self.vertexes.index(vertex)
    except ValueError:
      return [vertex]

    parent = index//2
    left_child = index*2
    right_child = index*2+1

    possibilities = set([parent, index, left_child, right_child])
    result = list(map(lambda v: self.vertexes[v], filter(
        lambda v: 0 <= v and v < len(self.vertexes), possibilities)))
    return result

  def describe(self):
    return f"Bináris fa, szülő = index/2, gyerekek = index*2 és index*2 + 1"
