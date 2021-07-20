from commands.latex.wrap_standalone_latex import wrap_standalone_latex


def vector2latex(vector):
  latex = []
  if vector.ndim != 1:
    raise Exception("Nem 1 dimenziós a vektor!")

  latex += ["$\\big($"]

  nums = map(lambda x: f'${x:.10f}$', vector)
  latex += [f"{', '.join(nums)}"]

  latex += ["$\\big)$"]
  return latex
