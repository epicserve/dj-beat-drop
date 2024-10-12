import argparse

from dj_beat_drop.new import handle_new


def main():
    parser = argparse.ArgumentParser(description="DJ Beat Drop")
    subparsers = parser.add_subparsers(dest="command")

    # Add 'new' subcommand
    new_parser = subparsers.add_parser("new", help="Create a new Django project.")
    new_parser.add_argument(
        "name",
        type=str,
        help="Project name (e.g. 'example_project' or 'example-project').",
    )
    new_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the project directory if it already exists.",
    )

    args = parser.parse_args()

    if args.command == "new":
        handle_new(args.name, args.overwrite)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
