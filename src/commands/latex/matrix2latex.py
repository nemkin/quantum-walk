def insert_after(list, steps, inserted):
  for index, element in enumerate(list):
    yield element
    if (index+1) % steps == 0:
      yield inserted


def matrix2latex(matrix, divider_steps):
  latex = []
  rows, cols = matrix.shape

  latex += ["\\documentclass[border=1em]{standalone}"]
  latex += [""]
  latex += ["% Table setup"]
  latex += ["\\usepackage[table]{xcolor} % Cell colors"]
  latex += [""]
  latex += ["\\begin{document}"]
  latex += [""]
  latex += ["$"]
  latex += ["\\left("]

  column_definition = ''.join(insert_after(['c']*cols, divider_steps, '|'))
  latex += [f"\\begin{{array}}{{{column_definition}}}"]

  latex_rows = []
  for i in range(rows):
    nums = map(lambda x: f'{x:.6f}', matrix[i, :])
    latex_rows += [f"{' & '.join(nums)} \\\\"]

  latex += insert_after(latex_rows, divider_steps, "\\hline")
  latex += ["\\end{array}"]
  latex += ["\\right)"]
  latex += ["$"]
  latex += [""]
  latex += ["\\end{document}"]

  return latex
