import subprocess


def run_bash(command, location):
  process = subprocess.Popen(
      command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=location)
  out, err = process.communicate()
  if process.returncode != 0:
    print("Out:")
    print("------------")
    print(out.decode())
    print(f"Error ({process.returncode}):")
    print("------------")
    print(err.decode())
