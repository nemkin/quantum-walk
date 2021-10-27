from commands.latex.vector2latex import vector2latex
import numpy as np


def eigens2latex(eigens):
  latex = []
  values = eigens.get_eigen_values()

  for value in sorted(values, reverse=True):
    latex += [f"${value:.10f}$:\\"]
    angle = np.angle(value, deg=True)
    if angle != 0:
        osztva = 360 / angle
    else:
        osztva = np.Inf
    latex += [f"Angle: ${angle:.10f}$ \\"]
    latex += [f"360 / angle: ${osztva:.10f}$\\"]
    latex += ["\\begin{itemize}"]
    vectors = eigens.get_eigen_vectors_for(value)
    for vector in vectors:
      latex += ["\\item"]
      latex += vector2latex(vector)
    latex += ["\\end{itemize}"]

  return latex
