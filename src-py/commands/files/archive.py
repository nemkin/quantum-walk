import os
from config import Config


def archive():
  try:
    os.makedirs(Config.new_root)
  except:
    pass

  try:
    os.makedirs(Config.archive_root)
  except:
    pass

  file_names = os.listdir(Config.new_root)
  if len(file_names) < 1:
    return

  archive_dir = Config.archive_root / '_'.join(file_names[0].split('_')[:7])
  try:
    os.makedirs(archive_dir)
  except:
    pass

  for file_name in file_names:
    (Config.new_root / file_name).rename(archive_dir / file_name)
