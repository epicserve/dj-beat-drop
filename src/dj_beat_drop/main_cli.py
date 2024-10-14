import argparse

import requests

from dj_beat_drop.new import handle_new
from pkg_resources import get_distribution, parse_version

from dj_beat_drop.utils import green


def get_ascii_logo():
    logo = r"""
   ___     __  ___           __    ___              
  / _ \__ / / / _ )___ ___ _/ /_  / _ \_______  ___ 
 / // / // / / _  / -_) _ `/ __/ / // / __/ _ \/ _ \
/____/\___/ /____/\__/\_,_/\__/ /____/_/  \___/ .__/
                                             /_/
"""
    return logo


def check_version():
    package_name = "dj-beat-drop"
    current_version = get_distribution(package_name).version

    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    latest_version = response.json()["info"]["version"]

    if parse_version(current_version) < parse_version(latest_version):
        green(
            f"\033[0;33m\nA new version of {package_name} is available ({latest_version}). You are using {current_version}. To update, run:\n\033[0m"
        )
        print(f"  pip install --upgrade {package_name}\n")


def main():
    print(f"\033[38;2;255;165;0m{get_ascii_logo()}\033[0m")
    check_version()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    # Add 'new' subcommand
    new_parser = subparsers.add_parser("new", help="Create a new Django project.")
    new_parser.add_argument(
        "name",
        type=str,
        nargs="?",
        help="Project name (e.g. 'example_project' or 'example-project').",
    )
    new_parser.add_argument(
        "--lts",
        action="store_true",
        help="Use the latest LTS version of Django.",
    )
    new_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the project directory if it already exists.",
    )

    args = parser.parse_args()

    if args.command == "new":
        handle_new(args.name, args.lts, args.overwrite)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
