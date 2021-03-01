import os
import random
import progressbar
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from generate_graph import generate

now = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")

def move(pos, N, graph):
  pos = np.random.choice(N, 1, p=graph[pos,:].todense().flat)
  return pos

def simulate(N,simulations,steps,w,density):
  graph = generate(N,w,density)
  start = N // 2

  print(f"N={N}, w={w}, density={density}, start={start}, simulations={simulations}, steps={steps}")

  counts = np.zeros([steps+1, N])
  counts += 0.01
  for _ in progressbar.progressbar(range(simulations)):
    pos = start
    counts[0,pos] += 1
    for step_i in range(1,steps+1):
      pos = move(pos, N, graph)
      counts[step_i,pos] += 1

  steps_Y = np.arange(-0.5, steps, 1)
  vertexes_X = np.arange(-0.5, N-1, 1)

  fig, ax = plt.subplots(1,1,figsize=(6,9))
  pcm = ax.pcolormesh(
      vertexes_X,
      steps_Y,
      counts,
      cmap='plasma',
      shading='auto',
      norm=colors.LogNorm(vmin=counts.min(), vmax=counts.max())
  )
  ax.set_title(f'Csúcsok száma: {N}\nSzélesség: {w}\nVéletlen élek: {density}\nKiindulási csúcs: {start}\nFutások darabszáma: {simulations}\nLépések száma egy futásban: {steps}\n', loc='left')
  ax.set_xlabel('Csúcsindexek')
  ax.set_ylabel('Lépések')
  fig.colorbar(pcm, ax=ax, extend='max')
  filename = f'{now}_counts_circle_N_{N}_w_{w}_density_{density}_start_{start}_simulations_{simulations}_steps_{steps}'
  fig.savefig(
      f'{filename}.png',
      dpi=600,
      bbox_inches='tight'
  )
  plt.close(fig)
  with open(f'{filename}_graph.txt', 'w') as f:
    f.write(str(graph))

if __name__ == '__main__':
    # Csúcsok száma, futások száma, lépések száma, szélesség, density
    simulate(101, 1, 1000, 1, 0)
    simulate(101, 1, 1000, 2, 0)
    simulate(101, 1, 1000, 3, 0)
    simulate(101, 1, 1000, 3, 0.2)

    simulate(101, 10, 1000, 1, 0)
    simulate(101, 10, 1000, 2, 0)
    simulate(101, 10, 1000, 3, 0)
    simulate(101, 10, 1000, 3, 0.2)

    simulate(101, 1000, 1000, 1, 0)
    simulate(101, 1000, 1000, 2, 0)
    simulate(101, 1000, 1000, 3, 0)
    simulate(101, 1000, 1000, 3, 0.2)

