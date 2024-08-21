import pathlib as p
import string
import subprocess
import sys

from bump_version import main as _bump_version
from bump_version import version_file

ALLOWED_CHARS = string.ascii_letters + string.digits + '-_/\\.: '

def print_error(msg: str, *, and_exit: bool = True):
  print(f'\nUPLOAD FAILED: {msg}\n')
  if and_exit:
    sys.exit(1)

def get_valid_git_path() -> str:
  git_add_raw_path = version_file.absolute().__str__()
  git_add_path = ''.join(filter(lambda x: x in ALLOWED_CHARS, git_add_raw_path))

  if git_add_path != git_add_raw_path:
    print_error(f'Invalid characters in git add path for the version.py file: {git_add_raw_path!r}.')
    sys.exit(1)

  return git_add_path

def bump_version() -> str:
  version_after_bump = _bump_version()
  return ''.join(filter(lambda x: x in ALLOWED_CHARS, version_after_bump))

def rm_r_dist_directory():
  dist_folder = p.Path('./dist')

  if not dist_folder.is_dir():
    print_error('./dist/ folder not found, are you in the correct directory?')
    sys.exit(1)

  for file in dist_folder.iterdir():
    file.unlink()

def run_shell_commands(*, version_after_bump: str, git_add_path: str):
  cmds = f"""
git add .
git commit -m "commit files not committed before upload to version {version_after_bump}"
git add {git_add_path}
git commit -m "bump version to {version_after_bump}"
git push
py -m build
py -m twine upload dist/*
""".strip().split('\n')

  for cmd in cmds:
    # input(f'RUNNING: {cmd!r}\n>>> ')
    subprocess.run(cmd, shell=True)

def main():
  version_after_bump = bump_version()
  valid_git_path = get_valid_git_path()
  rm_r_dist_directory()
  run_shell_commands(
    version_after_bump=version_after_bump,
    git_add_path=valid_git_path
  )


if __name__ == '__main__':
  main()
