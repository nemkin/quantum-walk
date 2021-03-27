class BinaryTree(object):
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
        result = list(map(lambda v: self.vertexes[v], filter(lambda v: 0 <= v and v < len(self.vertexes), possibilities)))        
        return result

