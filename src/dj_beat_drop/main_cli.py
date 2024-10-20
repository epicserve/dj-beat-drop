import importlib.metadata

import requests
import typer
from packaging.version import parse

from dj_beat_drop.new import handle_new
from dj_beat_drop.utils import color


def get_ascii_logo():
    logo = r"""
   ___     __  ___           __    ___
  / _ \__ / / / _ )___ ___ _/ /_  / _ \_______  ___
 / // / // / / _  / -_) _ `/ __/ / // / __/ _ \/ _ \
/____/\___/ /____/\__/\_,_/\__/ /____/_/  \___/ .__/
                                             /_/     """
    return logo


def get_current_version():
    return importlib.metadata.version("dj-beat-drop")


main_command = typer.Typer(no_args_is_help=True)


def print_version(value: bool):
    if value:
        print(f"Version {get_current_version()}")
        raise typer.Exit()


def check_version():
    package_name = "dj-beat-drop"
    current_version = get_current_version()

    response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=10)
    latest_version = response.json()["info"]["version"]

    if parse(current_version) < parse(latest_version):
        color.green(
            f"\033[0;33m\nA new version of {package_name} is available ({latest_version}). You are using "
            f"{current_version}. To update, run:\n\033[0m"
        )
        print(f"  pip install --upgrade {package_name}\n")


@main_command.callback()
def main_callback(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=print_version,
        is_eager=True,
        help="Show the application's version and exit.",
    ),
):
    pass


@main_command.command()
def new(
    name: str | None = typer.Argument(None, help="Project name (e.g. 'example_project' or 'example-project')."),
    use_lts: bool = typer.Option(False, "--lts", help="Use the latest LTS version of Django."),
    overwrite: bool = typer.Option(False, "--overwrite", help="Overwrite the project directory if it already exists."),
):
    handle_new(name, use_lts, overwrite)


def main():
    color.orange(get_ascii_logo())
    check_version()
    main_command()


if __name__ == "__main__":
    main()
