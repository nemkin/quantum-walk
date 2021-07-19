from commands.latex.wrap_standalone_latex import wrap_standalone_latex
from commands.latex.matrix2latex import matrix2latex_format


def eigens2latex(eigens):
  latex = []
  values = eigens.get_eigen_values()

  for value in values:
    latex += [f"${value:.6f}$:"]
    latex += ["\\newline"]
    vectors = eigens.get_eigen_vectors_for(value)
    for vector in vectors:
      latex += matrix2latex_format(vector)
      latex += ["\\newline"]

  return wrap_standalone_latex(latex)
