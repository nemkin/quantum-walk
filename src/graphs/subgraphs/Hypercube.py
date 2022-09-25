from commands.maths.is_power_of_2 import is_power_of_2
from graphs.subgraphs.SubGraph import SubGraph
import math


class Hypercube(SubGraph):

  def __init__(self, vertexes):
    self.vertexes = list(vertexes)
    if not is_power_of_2(len(self.vertexes)):
      raise "Nem 2 hatvány a csúcsok száma!"
    self.bits = int(math.log2(len(self.vertexes)))

  def flip_bit(number, bit_index):
    return number ^ (1 << bit_index)

  def neighbours(self, vertex):
    try:
      index = self.vertexes.index(vertex)
    except ValueError:
      return []

    return list(map(lambda i: self.vertexes[i],
                    [Hypercube.flip_bit(index, bit_index)
                     for bit_index in range(self.bits)]))

  def describe(self):
    return f"Hiperkocka {self.bits} bittel"
