from commands.latex.vector2latex import vector2latex
import numpy as np


def eigens2latex(eigens):
  latex = []
  values = eigens.get_eigen_values()
  latex += ["\\begin{itemize}"]
  for value in sorted(values, reverse=True):
    angle = np.angle(value, deg=True)
    if angle != 0:
        osztva = 360 / angle
    else:
        osztva = np.Inf
    latex += [f"\\item ${value:.10f}$:\\"]
    latex += ["\\begin{itemize}"]
    latex += [f"  \\item angle: ${angle:.10f}$ \\"]
    latex += [f"  \\item 360 / angle: ${osztva:.10f}$\\"]
    latex += ["\\end{itemize}"]
    
    # vectors = eigens.get_eigen_vectors_for(value)
    # for vector in vectors:
    # latex += vector2latex(vector)
    
    latex += ["\\end{itemize}"]

  return latex
