class Circle(object):
    vertexes = []
    neighbour_distances = []

    def __init__(self, vertexes, neighbour_distances):
        self.vertexes = list(vertexes)
        self.neighbour_distances = neighbour_distances

    def neighbours(self, vertex):
        index = self.vertexes.index(vertex)
        return map(lambda dist: self.vertexes[(dist + index) % len(self.vertexes)], self.neighbour_distances)
