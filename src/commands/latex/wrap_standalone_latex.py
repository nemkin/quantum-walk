def wrap_standalone_latex(inner_latex):
  latex = []
  latex += ["\\documentclass[border=1em]{standalone}"]
  latex += [""]
  latex += ["% Table setup"]
  latex += ["\\usepackage[table]{xcolor} % Cell colors"]
  latex += [""]
  latex += ["\\begin{document}"]
  latex += [""]
  latex += inner_latex
  latex += [""]
  latex += ["\\end{document}"]
  return latex
