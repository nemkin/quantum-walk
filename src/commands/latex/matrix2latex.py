from commands.latex.wrap_standalone_latex import wrap_standalone_latex


def insert_every(list, inserted, steps=None):
  for index, element in enumerate(list):
    yield element
    if steps != None and (index+1) % steps == 0 and (index+1) != len(list):
      yield inserted


def matrix2latex_format(matrix, divider_steps=None):
  latex = []
  if matrix.ndim == 1:
    n = matrix.shape[0]
    matrix = matrix.reshape(1, n)
  rows, cols = matrix.shape

  latex += ["$"]
  latex += ["\\left("]

  column_definition = ''.join(insert_every(['c']*cols, '|', divider_steps))
  latex += [f"\\begin{{array}}{{{column_definition}}}"]

  latex_rows = []
  for i in range(rows):
    nums = map(lambda x: f'{x:.6f}', matrix[i, :])
    latex_rows += [f"{' & '.join(nums)} \\\\"]

  latex += insert_every(latex_rows, "\\hline", divider_steps)

  latex += ["\\end{array}"]
  latex += ["\\right)"]
  latex += ["$"]
  return latex


def matrix2latex_document(matrix, divider_steps=None):
  return wrap_standalone_latex(matrix2latex_format(matrix, divider_steps))
