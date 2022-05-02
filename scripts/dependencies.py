import pathlib
import subprocess
import sys
import typing


def main() -> int:
    return_code = 0
    return_code += poetry_update()
    return_code += pre_commit_update()
    if not return_code:
        commit_and_push()
    return return_code


def poetry_update():
    return _run_command(("poetry", "update"))


def pre_commit_update():
    return _run_command(("pre-commit", "autoupdate", "--bleeding-edge"))


def commit_and_push():
    return (
        _run_command(("git", "add", "poetry.lock", ".pre-commit-config.yaml"))
        + _run_command(("git", "commit", "-m", ":rocket: [Auto] - `dependencies rollup`."))
        + _run_command(("git", "push"))
    )


def _run_command(command: typing.Tuple[str, ...]) -> int:
    """
    Run a command and return the subprocess exit code.
    :param command: Command to run.
    :return:
    """
    return subprocess.run(command, stdout=sys.stdout, stderr=subprocess.STDOUT).returncode


if __name__ == "__main__":
    """
    A rather naive utility script for updating poetry and pre-commit dependencies.
    From the root directory of `asserto`:
        python scripts/dependencies.py
    """
    raise SystemExit(main())
