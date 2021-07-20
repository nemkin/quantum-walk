from commands.latex.vector2latex import vector2latex


def eigens2latex(eigens):
  latex = []
  values = eigens.get_eigen_values()

  for value in sorted(values, reverse=True):
    latex += [f"${value:.10f}$:"]
    latex += ["\\begin{itemize}"]
    vectors = eigens.get_eigen_vectors_for(value)
    for vector in vectors:
      latex += ["\\item"]
      latex += vector2latex(vector)
    latex += ["\\end{itemize}"]

  return latex
