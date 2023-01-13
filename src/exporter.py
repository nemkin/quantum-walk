from commands.latex.matrix2latex import matrix2latex_document
from commands.latex.eigens2latex import eigens2latex
from commands.maths.eigens import Eigens
from commands.latex.create_latex import create_latex
from commands.bash.run_bash import run_bash
from commands.print.matrix2string import matrix2string
from locations import RunLocations
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import cm

from tqdm import tqdm
from config import Config

from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

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
    fig.savefig(filename.vector_image())
    plt.close(fig)

    with open(filename.text(), "w") as f:
      f.write(np.array2string(y))

  def draw_adj(self, adj, filename):
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    X, Y = np.meshgrid(range(adj.shape[0]+1), range(adj.shape[1]+1))

    absadj = np.absolute(adj)
    ax.pcolormesh(
        X,
        Y,
        absadj,
        cmap='rainbow',
        shading='auto',
        linewidths=1,
        snap=True,
        norm=colors.LogNorm(0.0001,1)
    )
    ax.xaxis.tick_top()
    ax.invert_yaxis()

    fig.tight_layout()
    fig.savefig(filename.image())
    fig.savefig(filename.vector_image())
    plt.close(fig)

    with open(filename.text(), "w") as f:
      f.write(np.array2string(adj))

    with open(filename.numpy(), 'wb') as f:
      np.save(f, adj)

  def draw_adj_3d(self, adj, filename):
    fig, ax = plt.subplots(dpi=300,
                           subplot_kw={"projection": "3d"})
    X, Y = np.meshgrid(range(adj.shape[0]), range(adj.shape[1]))
    ax.plot_surface(
        X,
        Y,
        adj,
        cmap=cm.coolwarm,
        linewidth=0,
        antialiased=False)
    # ax.set_zlim(0, 1)

    # ax.xaxis.tick_top()
    # ax.invert_yaxis()

    fig.tight_layout()
    fig.savefig(filename.image())
    fig.savefig(filename.vector_image())
    plt.close(fig)

    with open(filename.text(), "w") as f:
      f.write(np.array2string(adj))

    with open(filename.numpy(), 'wb') as f:
      np.save(f, adj)

  def draw(self, simulation, simloc):
    simulator = simulation["simulator"]
    counts = simulation["counts"]

#    size = int(np.sqrt(counts.shape[1]))
#    for i in range(counts.shape[0]):
#      self.draw_adj_3d(
#          counts[i, :].reshape((size, size)), simloc.counts(i))
#
#    return
    smaller = 2 * self.run.N
    steps_smaller = simulator.steps - smaller

    steps_Y_smaller = np.arange(-0.5 + smaller, simulator.steps, 1)
    counts_smaller = counts[smaller:]

    steps_Y = np.arange(-0.5, simulator.steps, 1)
    vertexes_X = np.arange(0, self.run.N, 1)

    div = np.gcd(self.run.N, simulator.steps)
    x = 5 # self.run.N // div # 6
    y = 20 # simulator.steps // div # 5

    N = 256
    cmap = cm.get_cmap('rainbow', 256)
    vals = cmap(np.linspace(0, 1, N))
    red = np.array([1, 0, 0, 1])
    #vals[-2:, :] = red
    #vals[:, 0] = np.linspace(90/256, 1, N)
    #vals[:, 1] = np.linspace(1, 0, N)
    #vals[:, 2] = np.linspace(1, 0, N)
    newcmp = ListedColormap(vals)
   
    fig, ax = plt.subplots(1, 1, figsize=(x, y))
    pcm = ax.pcolor(
        vertexes_X,
        steps_Y,
        counts,
        cmap='rainbow', # newcmp,
        shading='auto',
        linewidths=1,
        snap=True,
        # vmin=0,
        # vmax=1
        norm=colors.LogNorm(vmin=np.min(counts[np.nonzero(counts)]), vmax=counts.max())
        #norm=colors.LogNorm(vmin=0.1, vmax=1.0)
    )
    ax.set_title(simulator.describe())
    ax.set_xlabel('Vertices')
    ax.set_ylabel('Steps')

    ax.set_xticks(np.arange(0, self.run.N, 1), minor=False)
    ax.set_xticklabels(list(range(self.run.N)))
    
    fig.tight_layout()
    fig.colorbar(pcm)

    fig.savefig(simloc.counts().image())
    fig.savefig(simloc.counts().vector_image())
    plt.close(fig)

    # Counts_short
    #if steps_smaller > 0:
    #  div = np.gcd(self.run.N, steps_smaller)
    #  x = 6  # self.run.N // div
    #  y = 12  # steps_smaller // div
    #
    #  fig, ax = plt.subplots(1, 1, figsize=(x, y))
    #  pcm = ax.pcolor(
    #      vertexes_X,
    #      steps_Y_smaller,
    #      counts_smaller,
    #      cmap='rainbow',
    #      shading='auto',
    #      linewidths=1,
    #      snap=True,
    #      norm=colors.LogNorm(vmin=np.min(
    #          counts_smaller[np.nonzero(counts_smaller)]), vmax=counts_smaller.max())
    #  )
    #  ax.set_title(simulator.describe())
    #  ax.set_xlabel('Vertices')
    #  ax.set_ylabel('Steps')
    #  fig.tight_layout()

    #  fig.savefig(simloc.counts_short().image())
    #  fig.savefig(simloc.counts_short().vector_image())
    #  plt.close(fig)

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
      if i != 0:
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
    self.description += ["\\usepackage[english]{babel} % Babel for Hungarian"]
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
    create_latex(self.loc.graph_adj().latex(),
                 matrix2latex_document(self.run.graph_adj))

    self.description += ["\\section{Graph}"]
    self.description += ["\\subsection{Adjacency matrix}"]
    self.add_graphics(self.loc.graph_adj(is_latex=True).vector_image(),
                      "Graph adjacency matrix")

  def add_coin_faces(self):
    for i, coin_face in tqdm(enumerate(self.run.coin_faces), desc="Export coin faces", leave=False):
      self.draw_adj(coin_face, self.loc.coin_face(i))

      self.description += ["\\subsection{Coin face}"]
      self.add_graphics(self.loc.coin_face(i, is_latex=True).vector_image(),
                        f"{i}th coin face adjacency matrix")

  def add_sub_graphs(self):
    for i, sub_graph in tqdm(enumerate(self.run.sub_graphs), desc="Export sub graphs", leave=False):

      self.draw_adj(sub_graph["adj"], self.loc.subgraph_adj(i))

      self.description += ["\\subsection{Subgraph}"]
      self.description += [sub_graph["describe"]]
      self.add_graphics(self.loc.subgraph_adj(i, is_latex=True).vector_image(),
                        f"{i}th subgraph adjacency matrix")

  def add_simulations(self):
    self.description += ["\\section{Simulations}"]

    for i, simulation in tqdm(enumerate(self.run.simulations),  desc="Export simulations", leave=False):
      simulator = simulation["simulator"]
      counts = simulation["counts"]
      mixing_time = simulation["mixing_time"]
      hitting_time = simulation["hitting_time"]
      simulation_matrix = simulation["simulation_matrix"]
      eigens = simulation["eigens"]

      periodicity = []
      for index, row in enumerate(counts):
          if np.allclose(row, counts[0]):
              periodicity.append(index)
      # np.where((counts == counts[0])).all(axis=1)
      with open(self.loc.simulation(i).periodicity().text(), "w") as f:
        f.write(' '.join(map(str, periodicity)))

      self.draw(simulation, self.loc.simulation(i))
      self.draw_graphics(
          mixing_time,
          simulator.describe(),
          "Steps",
          "Euclidean distance between the last and the current distributions",
          self.loc.simulation(i).mixing_time())
      self.draw_graphics(
          hitting_time,
          simulator.describe(),
          "Vertices",
          "First non-zero step",
          self.loc.simulation(i).hitting_time())

      self.description += [f"\\subsection{{{simulator.describe()}}}"]
      self.description += [f"Starting vertex: {simulator.start}"]
      self.description += [f"Walkers: {simulator.simulations}"]
      self.description += [f"Steps: {simulator.steps}"]

      self.add_graphics(
          self.loc.simulation(i, is_latex=True).counts().vector_image(), f"{i}th simulation")
      #self.add_graphics(
      #    self.loc.simulation(i, is_latex=True).counts_short().vector_image(), f"{i}th simulation, removing the beginning")
      self.add_graphics(
          self.loc.simulation(i, is_latex=True).mixing_time().vector_image(), f"{i}th simulation mixing time")
      self.add_graphics(
          self.loc.simulation(i, is_latex=True).hitting_time().vector_image(), f"{i}th simulation hitting time")

      self.description += ["\\subsection{Eigenvalues, eigenvectors}"]
      self.description += eigens2latex(Eigens(simulation_matrix))

      if simulator.is_quantum():
        size = simulator.coin.size
      else:
        size = None

      self.draw_adj(simulation_matrix,
                    self.loc.simulation(i).simulation_matrix())
      # create_latex(self.loc.simulation(i).simulation_matrix().latex(),
      #              matrix2latex_document(simulation_matrix, size))

      self.description += ["\\section{Simulation matrix}"]
      self.description += [f"\\subsection{{{i}.th simulation matrix}}"]
      self.add_graphics(self.loc.simulation(i, is_latex=True).simulation_matrix().vector_image(),
                        f"{i}th simulation matrix")

      if simulator.is_quantum():  # TODO is quantum miert nem jo itt?
        create_latex(
            self.loc.simulation(i).coin_start().latex(),
            matrix2latex_document(simulator.coin.start()))

        self.description += ["\\subsection{Coin eigenvalues, eigenvectors}"]
        self.description += eigens2latex(Eigens(simulator.coin.step()))

        create_latex(
            self.loc.simulation(i).coin_step().latex(),
            matrix2latex_document(simulator.coin.step()))

  def add_end(self):
    self.description += ["\\end{document}"]

  def create_latex(self):
    create_latex(self.loc.root/(f'{self.run.filename}.tex'), self.description)

  def export(self):
    self.add_begin()
    self.add_graph()
    self.add_coin_faces()
    self.add_sub_graphs()
    self.add_simulations()
    self.add_end()

    self.create_latex()
