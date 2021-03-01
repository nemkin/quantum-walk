import os
import random
import progressbar
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

now = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
os.mkdir(now)

def move(pos, N, graph):
  pos = np.random.choice(N, 1, p=graph[pos,:].flatten())
  return pos

def simulate(N,simulations,steps,connections,random_factor):
  graph = generate_graph(N,connections,random_factor)
  start = N // 2

  print(f"N={N}, start={start}, simulations={simulations}, steps={steps}")

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
  ax.set_title(f'Csúcsok száma: {N}\nKiindulási csúcs: {start}\nFutások darabszáma: {simulations}\nLépések száma egy futásban: {steps}\n', loc='left')
  ax.set_xlabel('Csúcsindexek')
  ax.set_ylabel('Lépések')
  fig.colorbar(pcm, ax=ax, extend='max')
  fig.savefig(
      f'{now}/counts_circle_N_{N}_start_{start}_simulations_{simulations}_steps_{steps}.png',
      dpi=600,
      bbox_inches='tight'
  )
  plt.close(fig)

if __name__ == '__main__':
    # Csúcsok száma, futások száma, lépések száma 
    simulate(101,10,10000,1,0)
    simulate(101,1000,1000,1,0)
    # simulate(1001, 1000, 10000)

