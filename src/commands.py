import subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import pydng
import time
import os
import shutil
from tqdm import tqdm

new_root = "../generations/new"
archive_root = "../generations/archives"
np.set_printoptions(threshold=np.inf)


def print_debug(graph, filename):
  coin_faces = graph.coin_faces()
  with open(f"{filename}_coin_faces.txt", "w") as f:
    for coin_face in coin_faces:
      f.write(np.array2string(coin_face))
      f.write("\n\n")
      f.write(np.array2string(coin_face.sum(axis=0)))
      f.write("\n")
      f.write(np.array2string(coin_face.sum(axis=1)))
      f.write("\n\n\n")


def draw_adj(adj, filename):
  fig, ax = plt.subplots(1, 1, figsize=(6, 6))
  X, Y = np.meshgrid(range(adj.shape[0]+1), range(adj.shape[1]+1))
  ax.pcolormesh(
      X,
      Y,
      adj,
      cmap='plasma',
      shading='auto',
      linewidths=1,
      snap=True,
      norm=colors.LogNorm(1, vmax=adj.max())
  )
  fig.tight_layout()
  fig.savefig(filename)
  plt.close(fig)


def draw_single(N, steps, counts, filename):
  vertexes_X = np.arange(-0.5, N-1, 1)

  fig, ax = plt.subplots(1, 1)
  pcm = ax.plot(
      vertexes_X,
      counts[N//2],
  )
  ax.set_xlabel('Csúcsindexek')
  ax.set_ylabel('Valószínűségek')
  fig.tight_layout()
  fig.savefig(f"{filename}_single.png")
  plt.close(fig)


def draw(N, steps, counts, filename):

  steps_Y = np.arange(-0.5, steps, 1)
  vertexes_X = np.arange(-0.5, N-1, 1)

  x = 6
  y = 12  # min(6*steps//N, 12)
  fig, ax = plt.subplots(1, 1, figsize=(x, y))
  pcm = ax.pcolor(
      vertexes_X,
      steps_Y,
      counts,
      cmap='plasma',
      shading='auto',
      linewidths=1,
      snap=True,
      norm=colors.LogNorm(0.001, vmax=counts.max())
  )
  ax.set_xlabel('Csúcsindexek')
  ax.set_ylabel('Lépések')
  fig.tight_layout()
  fig.savefig(filename)
  plt.close(fig)

  with open(f"{filename}_counts.txt", "w") as f:
    f.write(np.array2string(counts))

  with open(f"{filename}_count_sums.txt", "w") as f:
    f.write(np.array2string(counts.sum(axis=1)))

  # draw_single(N, steps, counts, filename)


def archive():
  try:
    os.makedirs(new_root)
  except:
    pass
  try:
    os.makedirs(archive_root)
  except:
    pass
  file_names = os.listdir(new_root)
  for file_name in file_names:
    shutil.move(os.path.join(new_root, file_name), archive_root)


def make_name():
  time_part = time.strftime('%Y_%m_%d__%H_%M_%S')
  unique_part = pydng.generate_name()
  return f"{time_part}_{unique_part}"


def run(graph, sim_configs):
  name = make_name()
  dir = f"{new_root}/{name}"
  os.makedirs(dir)

  description = []

  description += ["% Geometry setup"]
  description += ["\\documentclass[14pt,a4paper]{article}"]
  description += ["\\usepackage[margin=3cm]{geometry}"]
  description += [""]
  description += ["% Language setup"]
  description += ["\\usepackage[magyar]{babel} % Babel for Hungarian"]
  description += ["\\usepackage[T1]{fontenc} % Output character encoding"]
  description += ["\\usepackage[utf8]{inputenc} % Input character encoding"]
  description += [""]
  description += ["% Spacing setup"]
  description += ["\\setlength{\\parindent}{0pt} % No paragraph indenting"]
  description += ["\\setlength{\\parskip}{5pt} % Set spacing between paragraphs"]
  description += ["\\frenchspacing"]
  description += ["\\newcommand{\\rmspace}{\\vspace{-19pt}}"]
  description += [""]
  description += ["% Dependency setup"]
  description += ["\\usepackage{amsmath}"]
  description += ["\\usepackage{amssymb}"]
  description += ["\\usepackage{listings}"]
  description += ["\\usepackage{float}"]
  description += ["\\usepackage{graphicx}"]
  description += [""]
  description += ["% Title setup"]
  description += ["\\title{Gráfszimuláció}"]
  description += ["\\author{Nemkin Viktória}"]
  description += ["\date{}"]
  description += [""]
  description += ["% Document"]
  description += ["\\begin{document}"]
  description += ["\\maketitle"]

  description += ["\\section{Gráf}"]

  graph_file = 'graph.jpg'
  debug_file = 'graph'

  description += ["\\begin{figure}[H]"]
  description += ["\\centering"]
  description += [
      f"\\includegraphics[width = 0.7\\columnwidth]{{{graph_file}}}"]
  description += ["\\caption{Gráf szomszédossági mátrixa}"]
  description += ["\\end{figure}"]

  print_debug(graph, f'{dir}/{debug_file}')
  draw_adj(graph.adjacency_matrix(), f'{dir}/{graph_file}')
  N = graph.vertex_count()

  for i in tqdm(range(len(graph.sub_graphs)), leave=False):
    description += ["\\subsection{Részgráf}"]
    description += [graph.sub_graphs[i].describe()]
    sub_graph_file = f'subgraph_{i:02}.jpg'

    description += ["\\begin{figure}[H]"]
    description += ["\\centering"]
    description += [
        f"\\includegraphics[width = 0.7\\columnwidth]{{{sub_graph_file}}}"]
    description += [f"\\caption{{{i}. részgráf szomszédossági mátrixa}}"]
    description += ["\\end{figure}"]

    draw_adj(graph.sub_graphs[i].adjacency_matrix(
        N), f'{dir}/{sub_graph_file}')

  description += ["\\section{Szimulációk}"]

  for i in tqdm(range(len(sim_configs)),  leave=False):
    simulator, start, simulations, steps = sim_configs[i]

    description += [f"\\subsection{{{simulator.describe()}}}"]
    description += [f"Kezdőcsúcs: {start}"]
    description += [f"Bolyongók: {simulations}"]
    description += [f"Lépésszám: {steps}"]
    sim_file = f'sim{i:02}.jpg'

    description += ["\\begin{figure}[H]"]
    description += ["\\centering"]
    description += [
        f"\\includegraphics[width = 0.7\\columnwidth]{{{sim_file}}}"]
    description += [f"\\caption{{{i}. szimuláció}}"]
    description += ["\\end{figure}"]

    counts = simulator.simulate(graph, start, simulations, steps)
    draw(N, steps, counts, f'{dir}/{sim_file}')

  description += ["\\end{document}"]

  latex_file = f'{dir}/latex.tex'
  with open(latex_file, 'w') as f:
    f.writelines("\n".join(description))

  latexmk = ["latexmk", "-pdf", "-silent", latex_file, f"-outdir={dir}"]
  process = subprocess.Popen(latexmk, stdout=subprocess.PIPE)
  output, error = process.communicate()
