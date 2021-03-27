from graphs.Graph import Graph
from graphs.subgraphs.Circle import Circle
from simulators.classical import simulate_classical

graph = Graph()
circle = Circle(range(10), [-1, 0, 1])
graph.sub_graphs.append(circle)

simulate_classical(graph, 5, 10, 10)
