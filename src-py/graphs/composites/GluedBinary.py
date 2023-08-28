from graphs.Graph import Graph
from graphs.subgraphs.Bipartite import Bipartite
from graphs.subgraphs.Circle import Circle
from graphs.subgraphs.BinaryTree import BinaryTree


class GluedBinary(Graph):

  def __init__(self, binary_height):
    self.name = "Glued binary"
    size = 2**binary_height
    first = [0, size]
    second = [first[1], size*2]
    self.sub_graphs = [
        BinaryTree(
            range(first[0], first[1])
        ),
        BinaryTree(
            range(second[1] - 1, second[0] - 1, -1)
        ),
        Bipartite(
            range(first[1]-size//2, first[1]),
            range(second[0], second[0] + size//2)
        )
    ]
