from locations import RunLocations
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
    self.loc = RunLocations(run)
    self.description = []

  def draw_graphics(self, y, title, xlabel, ylabel, filename):
    N = len(y)
    x = np.arange(0, N, 1)
    fig, ax = plt.subplots(1, 1)
    pcm = ax.plot(x, y)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(ymin=0)

    fig.tight_layout()
    fig.savefig(filename.image())
    plt.close(fig)

    with open(filename.text(), "w") as f:
      f.write(np.array2string(y))

  def draw_adj(self, adj, filename):
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    X, Y = np.meshgrid(range(adj.shape[0]+1), range(adj.shape[1]+1))
    ax.pcolormesh(
        X,
        Y,
        adj,
        cmap='rainbow',
        shading='auto',
        linewidths=1,
        snap=True,
        norm=colors.LogNorm(vmin=np.min(adj[np.nonzero(adj)]), vmax=adj.max())
    )
    ax.xaxis.tick_top()
    ax.invert_yaxis()

    fig.tight_layout()
    fig.savefig(filename.image())
    plt.close(fig)

    with open(filename.text(), "w") as f:
      f.write(np.array2string(adj))

    with open(filename.numpy(), 'wb') as f:
      np.save(f, adj)

  def draw(self, simulation, simloc):
    simulator = simulation["simulator"]
    counts = simulation["counts"]

    smaller = 2 * self.run.N
    steps_smaller = simulator.steps - smaller

    steps_Y_smaller = np.arange(-0.5 + smaller, simulator.steps, 1)
    counts_smaller = counts[smaller:]

    steps_Y = np.arange(-0.5, simulator.steps, 1)
    vertexes_X = np.arange(-0.5, self.run.N-1, 1)

    div = np.gcd(self.run.N, simulator.steps)
    x = 6  # self.run.N // div
    y = 12  # simulator.steps // div

    fig, ax = plt.subplots(1, 1, figsize=(x, y))
    pcm = ax.pcolor(
        vertexes_X,
        steps_Y,
        counts,
        cmap='rainbow',
        shading='auto',
        linewidths=1,
        snap=True,
        norm=colors.LogNorm(vmin=np.min(
            counts[np.nonzero(counts)]), vmax=counts.max())
    )
    ax.set_title(simulator.describe())
    ax.set_xlabel('Csúcsindexek')
    ax.set_ylabel('Lépések')
    fig.tight_layout()

    fig.savefig(simloc.counts().image())
    plt.close(fig)

    if steps_smaller > 0:
      div = np.gcd(self.run.N, steps_smaller)
      x = 6  # self.run.N // div
      y = 12  # steps_smaller // div

      fig, ax = plt.subplots(1, 1, figsize=(x, y))
      pcm = ax.pcolor(
          vertexes_X,
          steps_Y_smaller,
          counts_smaller,
          cmap='rainbow',
          shading='auto',
          linewidths=1,
          snap=True,
          norm=colors.LogNorm(vmin=np.min(
              counts_smaller[np.nonzero(counts_smaller)]), vmax=counts_smaller.max())
      )
      ax.set_title(simulator.describe())
      ax.set_xlabel('Csúcsindexek')
      ax.set_ylabel('Lépések')
      fig.tight_layout()

      fig.savefig(simloc.counts_short().image())
      plt.close(fig)

    with open(simloc.counts().text(), "w") as f:
      f.write(np.array2string(counts))

    with open(simloc.counts().numpy(), 'wb') as f:
      np.save(f, counts)

  def add_graphics(self, file, caption):
    self.description += ["\\begin{figure}[H]"]
    self.description += ["\\centering"]
    self.description += [
        f"\\includegraphics[width = 0.7\\columnwidth]{{{file}}}"]
    self.description += [f"\\caption{{{caption}}}"]
    self.description += ["\\end{figure}"]

  def add_numbers(self, numbers):
    n = len(numbers)
    cols = 5
    self.description += ["\\begin{centering}"]
    self.description += [f"\\begin{{tabular}}{{{'|'.join(['r']*cols)}}}"]
    for i in range(0, n, cols):
      if i is not 0:
        self.description += ["\\hline"]
      end = i+cols if i+cols <= n else n
      nums = numbers[i:end]
      strings = map(lambda x: f'{x: .6f}', nums)
      self.description += [f"{' & '.join(strings)} \\\\"]
    self.description += ["\\end{tabular}"]
    self.description += ["\\end{centering}"]

  def add_begin(self):
    self.description += ["% Geometry setup"]
    self.description += ["\\documentclass[14pt,a4paper]{article}"]
    self.description += ["\\usepackage[margin=1.5cm]{geometry}"]
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
    self.description += [
        f"\\title{{{self.run.title} \\\\ \\large {self.run.subtitle}}}"]
    self.description += ["\\author{}"]
    self.description += ["\date{}"]
    self.description += [""]
    self.description += ["% Document"]
    self.description += ["\\begin{document}"]
    self.description += ["\\maketitle"]

  def add_graph(self):
    self.draw_adj(self.run.graph_adj, self.loc.graph_adj())

    self.description += ["\\section{Gráf}"]
    self.add_graphics(self.loc.graph_adj(latex=True).image(),
                      "Gráf szomszédossági mátrixa")
    self.description += ["\\subsection{Szomszédossági mátrix}"]

  def add_coin_faces(self):
    for i, coin_face in tqdm(enumerate(self.run.coin_faces), desc="Export coin faces", leave=False):
      self.draw_adj(coin_face, self.loc.coin_face(i))

      self.description += ["\\subsection{Érme oldal}"]
      self.add_graphics(self.loc.coin_face(i, latex=True).image(),
                        f"{i}. érmeoldal szomszédossági mátrixa")

  def add_sub_graphs(self):
    for i, sub_graph in tqdm(enumerate(self.run.sub_graphs), desc="Export sub graphs", leave=False):

      self.draw_adj(sub_graph["adj"], self.loc.subgraph_adj(i))

      self.description += ["\\subsection{Részgráf}"]
      self.description += [sub_graph["describe"]]
      self.add_graphics(self.loc.subgraph_adj(i, latex=True).image(),
                        f"{i}. részgráf szomszédossági mátrixa")

  def add_simulations(self):
    self.description += ["\\section{Szimulációk}"]

    for i, simulation in tqdm(enumerate(self.run.simulations),  desc="Export simulations", leave=False):
      simulator = simulation["simulator"]
      counts = simulation["counts"]
      mixing_time = simulation["mixing_time"]
      hitting_time = simulation["hitting_time"]
      eigens = simulation["eigens"]

      self.draw(simulation, self.loc.simulation(i))
      self.draw_graphics(
          mixing_time,
          simulator.describe(),
          "Lépések",
          "Egymás utáni eloszlások euklideszi távolsága",
          self.loc.simulation(i).mixing_time())
      self.draw_graphics(
          hitting_time,
          simulator.describe(),
          "Csúcsok",
          "Első nem 0 step",
          self.loc.simulation(i).hitting_time())

      self.description += [f"\\subsection{{{simulator.describe()}}}"]
      self.description += [f"Kezdőcsúcs: {simulator.start}"]
      self.description += [f"Bolyongók: {simulator.simulations}"]
      self.description += [f"Lépésszám: {simulator.steps}"]

      self.add_graphics(
          self.loc.simulation(i, latex=True).counts().image(), f"{i}. szimuláció")
      self.add_graphics(
          self.loc.simulation(i, latex=True).counts_short().image(), f"{i}. szimuláció levágva az elejét")
      self.add_graphics(
          self.loc.simulation(i, latex=True).mixing_time().image(), f"{i}. szimuláció mixing time")
      self.add_graphics(
          self.loc.simulation(i, latex=True).hitting_time().image(), f"{i}. szimuláció hitting time")

      self.description += ["\\subsection{Sajátértékek}"]
      self.add_numbers(sorted(eigens.keys(), reverse=True))

      if simulator.is_quantum():
        with open(self.loc.simulation(i).coin_start().text(), "w") as f:
          f.write(np.array2string(np.array(simulator.coin.start())))

        with open(self.loc.simulation(i).coin_step().text(), "w") as f:
          f.write(np.array2string(simulator.coin.step()))

  def add_end(self):
    self.description += ["\\end{document}"]

  def run_command(self, command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.loc.root)
    out, err = process.communicate()
    if process.returncode != 0:
      print("Out:")
      print("------------")
      print(out.decode())
      print(f"Error ({process.returncode}):")
      print("------------")
      print(err.decode())

  def create_latex(self):
    # TODO use Locations here too
    latex_file = f'{self.run.filename}.tex'
    with open(self.loc.root / latex_file, 'w') as f:
      f.writelines("\n".join(self.description))

    self.run_command(["latexmk", "-pdf", "-silent", latex_file])
    clean = True
    if clean:
      self.run_command(["latexmk", "-c"])

  def export(self):
    self.add_begin()
    self.add_graph()
    self.add_coin_faces()
    self.add_sub_graphs()
    self.add_simulations()
    self.add_end()

    self.create_latex()
