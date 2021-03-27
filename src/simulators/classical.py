import random

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import progressbar


def simulate_classical(graph, start, simulations, steps):
    for _ in progressbar.progressbar(range(simulations)):
        pos = start
        for step_i in range(1, steps + 1):
            options = list(graph.neighbours(pos))
            print(options)
            pos = random.choice(options)
            print(pos)
