import os
import re
import secrets
import shutil
import zipfile
from io import BytesIO

import requests


def green(text):
    print(f"\033[92m{text}\033[0m")


def red(text):
    print(f"\033[91m{text}\033[0m")


def get_latest_django_version():
    response = requests.get("https://pypi.org/pypi/Django/json")
    if response.status_code == 200:
        data = response.json()
        return data["info"]["version"]
    else:
        raise Exception("Failed to fetch the latest Django version")


def get_version(version):
    rtn = ".".join(version)
    mapping = {"alpha": "a", "beta": "b", "rc": "rc"}
    for key in mapping:
        if key in version:
            key_index = version.index(key)
            first_part = ".".join(version[: key_index - 1])
            return f"{first_part}{mapping[key]}{version[key_index + 1]}"
    print(rtn)
    return rtn


def get_secret_key():
    """
    Return a 50 character random string usable as a SECRET_KEY setting value.
    """
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    return "".join(secrets.choice(chars) for i in range(50))


def handle_new(name, overwrite):
    django_version = get_latest_django_version()
    docs_version = ".".join(django_version.split(".")[0:2])
    template_url = (
        f"https://github.com/django/django/archive/refs/tags/{django_version}.zip"
    )
    template_dir = (
        f"/tmp/django_template/django-{django_version}/django/conf/project_template"
    )
    project_dir = os.path.join(os.getcwd(), name)

    if os.path.exists(template_dir):
        shutil.rmtree(template_dir)

    if os.path.exists(project_dir):
        if overwrite is False:
            overwrite_response = input(
                f"The directory '{name}' already exists. Do you want to overwrite it? (yes/no): "
            )
            if (
                overwrite_response.lower() != "yes"
                and overwrite_response.lower() != "y"
            ):
                print("Operation cancelled.")
                return
        shutil.rmtree(project_dir)

    response = requests.get(template_url)
    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall("/tmp/django_template")

        config_dir = os.path.join(template_dir, "config")
        os.rename(os.path.join(template_dir, "project_name"), config_dir)
        shutil.copytree(template_dir, project_dir)

        # Rename .py-tpl files to .py
        for root, _, files in os.walk(project_dir):
            for file in files:
                if file.endswith(".py-tpl"):
                    old_file = os.path.join(root, file)
                    new_file = os.path.join(root, file[:-4])
                    os.rename(old_file, new_file)

        # Replace variables with values
        for root, _, files in os.walk(project_dir):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                content = content.replace("{{ project_name }}", "config")
                content = content.replace("{{ django_version }}", django_version)
                content = content.replace("{{ docs_version }}", docs_version)
                content = content.replace("{{ secret_key }}", get_secret_key())
                with open(file_path, "w") as f:
                    f.write(content)

        shutil.rmtree("/tmp/django_template")

        green(f"New Django project created at {project_dir}.\n")
        green("To get started, run the following commands:\n")
        print(f"cd {name}")
        print(f"uv add django~={django_version}")
        print("uv run manage.py migrate")
        print("uv run manage.py runserver")
    else:
        red("Failed to download the Django template.")
