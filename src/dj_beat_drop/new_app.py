import shutil
from pathlib import Path

import typer

from dj_beat_drop.utils import (
    color,
    overwrite_directory_prompt,
    rename_template_files,
    replace_variables_in_directory,
    snake_or_kebab_to_camel_case,
)


def create_new_app(
    app_rel_path: str = typer.Argument(..., help="App relative path (e.g. 'accounts' or 'apps/accounts')."),
) -> dict[str, str]:
    template_dir_src = Path(__file__).parent / "templates" / "app_template"

    # normalize to lowercase
    app_rel_path = app_rel_path.lower()

    app_directory = Path.cwd() / app_rel_path

    app_name = app_directory.name
    app_name_space = app_rel_path.replace("/", ".") if "/" in app_rel_path else app_name
    overwrite_directory_prompt(app_directory)
    shutil.copytree(template_dir_src, app_directory)
    rename_template_files(app_directory)
    template_context = {
        "app_name": app_name_space,
        "camel_case_app_name": snake_or_kebab_to_camel_case(app_name),
    }
    replace_variables_in_directory(app_directory, template_context)
    color.green(f"\nSuccessfully created app '{app_name}' in {app_directory}")

    # Reminder to register the app
    color.orange("\nRemember to add your app to INSTALLED_APPS in your project's settings:")
    print("\n    INSTALLED_APPS = [")
    print("        ...,")
    print(f"        '{app_name_space}',")
    print("    ]")

    return template_context
