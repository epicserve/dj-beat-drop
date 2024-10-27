import os
import re
import secrets
import shutil
from functools import lru_cache
from pathlib import Path

import requests
from InquirerPy import inquirer


class Color:
    ESCAPE = "\033[0m"

    @staticmethod
    def green(text):
        print(f"\033[92m{text}{Color.ESCAPE}")

    @staticmethod
    def red(text):
        print(f"\033[91m{text}{Color.ESCAPE}")

    @staticmethod
    def orange(text):
        print(f"\033[38;2;255;165;0m{text}{Color.ESCAPE}")


color = Color()


@lru_cache
def get_django_releases():
    response = requests.get("https://pypi.org/pypi/Django/json", timeout=10)
    if response.status_code == 200:
        data = response.json()
        return {"latest": data["info"]["version"], "releases": data["releases"]}
    else:
        raise Exception("Failed to fetch Django releases")


def get_latest_django_version():
    full_version = get_django_releases()["latest"]
    minor_version = ".".join(full_version.split(".")[0:2])
    return full_version, minor_version


def get_lts_django_version():
    release_data = get_django_releases()
    latest_version = release_data["latest"]
    latest_minor_version = ".".join(latest_version.split(".")[0:2])
    latest_split = latest_version.split(".")
    if latest_split[1] == "2":
        return latest_version, latest_minor_version

    releases = get_django_releases()["releases"]
    for release in reversed(releases):
        if "b" in release or "rc" in release or "a" in release:
            continue
        version_parts = release.split(".")
        if version_parts[1] == "2":
            return release, ".".join(version_parts[0:2])


def get_template_context(*, use_lts: bool):
    django_version, minor_version = get_latest_django_version()
    if use_lts is True:
        django_version, minor_version = get_lts_django_version()
    return {
        "project_name": "config",
        "django_version": django_version,
        "docs_version": minor_version,
        "secret_key": get_secret_key(),
    }


def get_secret_key():
    """Return a 50 character random string usable as a SECRET_KEY setting value."""
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    return "".join(secrets.choice(chars) for _ in range(50))


def rename_template_files(project_dir):
    # Rename .py-tpl files to .py
    for file in project_dir.rglob("*"):
        if file.is_file() is False:
            continue
        if file.name.endswith(".py-tpl"):
            os.rename(file, file.with_name(file.name[:-4]))


def overwrite_directory_prompt(directory: Path, skip_confirm_prompt: bool = False) -> bool:
    if directory.exists():
        if skip_confirm_prompt is False:
            overwrite_response = inquirer.confirm(
                message=f"The directory '{directory}' already exists. Do you want to overwrite it?",
                default=True,
            ).execute()
            if overwrite_response is False:
                color.red("Operation cancelled.")
                return
        shutil.rmtree(directory)


def replace_variables_in_directory(directory: Path, context: dict[str, str]):
    for file in directory.rglob("*"):
        if file.is_file() is False:
            continue
        with file.open() as f:
            content = f.read()
        for variable, value in context.items():
            content = content.replace(f"{{{{ {variable} }}}}", value)
        with file.open("w") as f:
            f.write(content)


def snake_or_kebab_to_camel_case(text):
    return "".join([word.capitalize() for word in re.split(r"[-_]", text)])
