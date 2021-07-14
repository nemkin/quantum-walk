from config import Config
import os
import shutil


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
  archive_dir = f"{Config.archive_root}/{'_'.join(file_names[0].split('_')[:7])}"
  os.makedirs(archive_dir)
  for file_name in file_names:
    shutil.move(os.path.join(Config.new_root, file_name), archive_dir)
