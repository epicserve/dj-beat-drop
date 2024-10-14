import os
import re
import secrets
import shutil

from InquirerPy import inquirer

from dj_beat_drop.utils import green, red, get_latest_django_version


def get_secret_key():
    """
    Return a 50 character random string usable as a SECRET_KEY setting value.
    """
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    return "".join(secrets.choice(chars) for i in range(50))


def rename_template_files(project_dir):
    # Rename .py-tpl files to .py
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".py-tpl"):
                old_file = os.path.join(root, file)
                new_file = os.path.join(root, file[:-4])
                os.rename(old_file, new_file)


def replace_variables(project_dir, context: dict[str, str]):
    for root, _, files in os.walk(project_dir):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                content = f.read()
            for variable, value in context.items():
                content = content.replace(f"{{{{ {variable} }}}}", value)
            with open(file_path, "w") as f:
                f.write(content)


def handle_new(name, overwrite):
    if name is None:
        name = inquirer.text("Project name:").execute()

    if re.match(r"^[-a-z_]+$", name) is None:
        red(
            "Invalid project name. Please use only lowercase letters, hyphens, and underscores."
        )
        return

    django_version, minor_version = get_latest_django_version()
    project_dir = os.path.join(os.getcwd(), name)
    template_dir_src = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "templates", minor_version
    )

    if os.path.exists(project_dir):
        if overwrite is False:
            overwrite_response = inquirer.confirm(
                message=f"The directory '{name}' already exists. Do you want to overwrite it?",
                default=True,
            ).execute()
            if overwrite_response is False:
                red("Operation cancelled.")
                return
        shutil.rmtree(project_dir)

    initialize_uv = inquirer.confirm(
        message="Initialize your project with UV?", default=True
    ).execute()

    shutil.copytree(template_dir_src, project_dir)
    os.rename(
        os.path.join(project_dir, "project_name"), os.path.join(project_dir, "config")
    )

    rename_template_files(project_dir)
    replace_variables(
        project_dir,
        {
            "project_name": "config",
            "django_version": django_version,
            "docs_version": minor_version,
            "secret_key": get_secret_key(),
        },
    )

    if initialize_uv is True:
        os.chdir(project_dir)
        os.system("uv init")
        os.system("rm hello.py")
        os.system(f"uv add django~='{minor_version}'")
        os.system("uv run manage.py migrate")

    green(f"New Django project created.\n")

    if initialize_uv is True:
        green("To start Django's run server:\n")
        print(f"cd {name}")
        print("uv run manage.py runserver")
