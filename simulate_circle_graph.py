import random
import progressbar
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

def move(pos, N):
  i = random.choice([-1, 0, 1])
  pos += i
  pos = pos % N
  return pos

def simulate(start, N, steps):
  pos = start
  for i in range(steps):
    pos = move(pos, N)
  return pos

def main():
  N = 101
  start = N // 2
  simulations = 1
  steps = 2000

  print(f"N={N}, start={start}, simulations={simulations}, steps={steps}")

  counts = np.zeros([steps+1, N])
  counts += 0.01
  for _ in progressbar.progressbar(range(simulations)):
    pos = start
    counts[0,pos] += 1
    for step_i in range(1,steps+1): 
      pos = move(pos, N)
      counts[step_i,pos] += 1

  print(counts)
  print(counts.min())

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
      f'counts_circle_N_{N}_start_{start}_simulations_{simulations}_steps_{steps}.png',
      dpi=600,
      bbox_inches='tight'
  )

if __name__ == '__main__':
    main()
