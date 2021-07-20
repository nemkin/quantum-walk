from commands.latex.vector2latex import vector2latex
import numpy as np


def eigens2latex(eigens):
  latex = []
  values = eigens.get_eigen_values()

  for value in sorted(values, reverse=True):
    latex += [f"${value:.10f}$:\\"]
    angle = np.angle(value, deg=True)
    osztva = 360 / angle
    latex += [f"Bezárt szög: ${angle:.10f}$ \\"]
    latex += [f"360 / bezárt szög: ${osztva:.10f}$\\"]
    latex += ["\\begin{itemize}"]
    vectors = eigens.get_eigen_vectors_for(value)
    for vector in vectors:
      latex += ["\\item"]
      latex += vector2latex(vector)
    latex += ["\\end{itemize}"]

  return latex
