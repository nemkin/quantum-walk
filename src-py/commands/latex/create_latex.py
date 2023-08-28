from pathlib import Path
from commands.bash.run_bash import run_bash


def create_latex(file, latex, clean=True):
  file = Path(file)
  dir = file.parents[0]
  filename = file.name
  with open(file, 'w') as f:
    f.writelines("\n".join(latex))
  run_bash(["latexmk", "-pdf", "-silent", filename], dir)
#  if clean:
#    run_bash(["latexmk", "-c"], dir)
