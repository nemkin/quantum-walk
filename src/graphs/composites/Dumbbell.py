from graphs.Graph import Graph
from graphs.subgraphs.Bipartite import Bipartite
from graphs.subgraphs.Circle import Circle


class Dumbbell(Graph):

  def __init__(self, cirlce_size, circle_width, connection_width):
    self.sub_graphs = [
        Circle(
            range(0, cirlce_size),
            range(-circle_width, circle_width+1)
        ),
        Circle(
            range(cirlce_size, 2 * cirlce_size),
            range(-circle_width, circle_width+1)
        ),
        Bipartite(
            range(cirlce_size - connection_width, cirlce_size),
            range(cirlce_size, cirlce_size + connection_width)
        )
    ]
