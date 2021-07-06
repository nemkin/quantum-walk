import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from tqdm import tqdm
from config import Config

np.set_printoptions(threshold=np.inf)


class Exporter:

  def __init__(self, run):
    self.run = run
    self.path = f"{Config.new_root}/{self.run.name}"
    self.description = []

  def full_path(self, filename):
    return f"{self.path}/{filename}"

  def draw_graphics(self, y, xlabel, ylabel, filename):
    N = len(y)
    x = np.arange(0, N, 1)
    fig, ax = plt.subplots(1, 1)
    pcm = ax.plot(x, y)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(f"{self.full_path(filename)}.jpg")
    plt.close(fig)

    with open(f"{self.full_path(filename)}.txt", "w") as f:
      f.write(np.array2string(y))

  def draw_adj(self, adj, filename):
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

    ax.xaxis.tick_top()
    ax.invert_yaxis()

    fig.tight_layout()

    fig.savefig(f"{self.full_path(filename)}.jpg")
    plt.close(fig)

    with open(f"{self.full_path(filename)}.txt", "w") as f:
      f.write(np.array2string(adj))

  def draw(self, simulation, filename):
    simulator = simulation["simulator"]
    counts = simulation["counts"]

    steps_Y = np.arange(-0.5, simulator.steps, 1)
    vertexes_X = np.arange(-0.5, self.run.N-1, 1)

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

    fig.savefig(f"{self.full_path(filename)}.jpg")
    plt.close(fig)

    with open(f"{self.full_path(filename)}.txt", "w") as f:
      f.write(np.array2string(counts))

  def add_graphics(self, file, caption):
    self.description += ["\\begin{figure}[H]"]
    self.description += ["\\centering"]
    self.description += [
        f"\\includegraphics[width = 0.7\\columnwidth]{{{file}}}"]
    self.description += [f"\\caption{{{caption}}}"]
    self.description += ["\\end{figure}"]

  def add_begin(self):
    self.description += ["% Geometry setup"]
    self.description += ["\\documentclass[14pt,a4paper]{article}"]
    self.description += ["\\usepackage[margin=3cm]{geometry}"]
    self.description += [""]
    self.description += ["% Language setup"]
    self.description += ["\\usepackage[magyar]{babel} % Babel for Hungarian"]
    self.description += [
        "\\usepackage[T1]{fontenc} % Output character encoding"]
    self.description += [
        "\\usepackage[utf8]{inputenc} % Input character encoding"]
    self.description += [""]
    self.description += ["% Spacing setup"]
    self.description += [
        "\\setlength{\\parindent}{0pt} % No paragraph indenting"]
    self.description += [
        "\\setlength{\\parskip}{5pt} % Set spacing between paragraphs"]
    self.description += ["\\frenchspacing"]
    self.description += ["\\newcommand{\\rmspace}{\\vspace{-19pt}}"]
    self.description += [""]
    self.description += ["% Dependency setup"]
    self.description += ["\\usepackage{amsmath}"]
    self.description += ["\\usepackage{amssymb}"]
    self.description += ["\\usepackage{listings}"]
    self.description += ["\\usepackage{float}"]
    self.description += ["\\usepackage{graphicx}"]
    self.description += [""]
    self.description += ["% Title setup"]
    self.description += ["\\title{Gráfszimuláció}"]
    self.description += ["\\author{Nemkin Viktória}"]
    self.description += ["\date{}"]
    self.description += [""]
    self.description += ["% Document"]
    self.description += ["\\begin{document}"]
    self.description += ["\\maketitle"]

  def add_graph(self):
    graph_file = 'graph'
    self.draw_adj(self.run.graph_adj, graph_file)

    self.description += ["\\section{Gráf}"]
    self.add_graphics(graph_file, "Gráf szomszédossági mátrixa")

  def add_coin_faces(self):
    for i, coin_face in tqdm(enumerate(self.run.coin_faces), desc="Export coin faces", leave=False):
      coin_face_file = f'coin_face_{i:02}'
      self.draw_adj(coin_face, coin_face_file)

      self.description += ["\\subsection{Érme oldal}"]
      self.add_graphics(
          coin_face_file, f"{i}. érmeoldal szomszédossági mátrixa")

  def add_sub_graphs(self):
    for i, sub_graph in tqdm(enumerate(self.run.sub_graphs), desc="Export sub graphs", leave=False):
      sub_graph_file = f'subgraph_{i:02}'
      self.draw_adj(sub_graph["adj"], sub_graph_file)

      self.description += ["\\subsection{Részgráf}"]
      self.description += [sub_graph["describe"]]
      self.add_graphics(
          sub_graph_file, f"{i}. részgráf szomszédossági mátrixa")

  def add_simulations(self):
    self.description += ["\\section{Szimulációk}"]

    for i, simulation in tqdm(enumerate(self.run.simulations),  desc="Export simulations", leave=False):
      simulator = simulation["simulator"]
      counts = simulation["counts"]
      mixing_time = simulation["mixing_time"]
      hitting_time = simulation["hitting_time"]

      sim_file = f'sim{i:02}'
      mix_time_file = f'{sim_file}_mixing_time'
      hit_time_file = f'{sim_file}_hitting_time'

      self.draw(simulation, sim_file)
      self.draw_graphics(
          mixing_time,
          "Lépések",
          "Egymás utáni eloszlások euklideszi távolsága",
          mix_time_file)
      self.draw_graphics(
          hitting_time,
          "Csúcsok",
          "Első nem 0 step",
          hit_time_file)

      self.description += [f"\\subsection{{{simulator.describe()}}}"]
      self.description += [f"Kezdőcsúcs: {simulator.start}"]
      self.description += [f"Bolyongók: {simulator.simulations}"]
      self.description += [f"Lépésszám: {simulator.steps}"]

      self.add_graphics(
          sim_file, f"{i}. szimuláció")
      self.add_graphics(
          mix_time_file, f"{i}. szimuláció mixing time")
      self.add_graphics(
          hit_time_file, f"{i}. szimuláció hitting time")

  def add_end(self):
    self.description += ["\\end{document}"]

  def create_latex(self):
    latex_file = self.full_path(f'{self.run.name}.tex')
    with open(latex_file, 'w') as f:
      f.writelines("\n".join(self.description))

    latexmk = ["latexmk", "-pdf", "-silent",
               latex_file, f"-outdir={self.path}"]
    process = subprocess.Popen(
        latexmk, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()

    if process.returncode != 0:
      print("Latexmk out:")
      print("------------")
      print(out.decode())
      print(f"Latexmk error ({process.returncode}):")
      print("------------")
      print(err.decode())

  def export(self):
    os.makedirs(self.path)

    self.add_begin()
    self.add_graph()
    self.add_coin_faces()
    self.add_sub_graphs()
    self.add_simulations()
    self.add_end()

    self.create_latex()
