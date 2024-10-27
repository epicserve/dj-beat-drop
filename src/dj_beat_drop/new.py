import os
import re
import shutil
from pathlib import Path

from InquirerPy import inquirer

from dj_beat_drop import utils
from dj_beat_drop.utils import color, overwrite_directory_prompt, rename_template_files, replace_variables_in_directory


def replace_settings_with_environs(content: str) -> str:
    rtn_val = content
    init_env = "# Initialize environs\n" "env = Env()\n" "env.read_env()"
    rtn_val = f"from environs import Env\n\n{rtn_val}"
    rtn_val = re.sub(r"(^BASE_DIR.+$)", rf"\1\n\n\n{init_env}", rtn_val, flags=re.MULTILINE)
    rtn_val = re.sub(
        r"^SECRET_KEY =.+$",
        'SECRET_KEY = env.str("SECRET_KEY")',
        rtn_val,
        flags=re.MULTILINE,
    )
    rtn_val = re.sub(r"^DEBUG =.+$", 'DEBUG = env.bool("DEBUG")', rtn_val, flags=re.MULTILINE)
    rtn_val = re.sub(
        r"^ALLOWED_HOSTS = .+$",
        'ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")',
        rtn_val,
        flags=re.MULTILINE,
    )
    rtn_val = re.sub(
        r"^DATABASES\s*=\s*\{.+?\}\n\}",
        r'DATABASES = {"default": env.dj_db_url("DATABASE_URL")}',
        rtn_val,
        flags=re.MULTILINE | re.DOTALL,
    )
    return rtn_val


def create_dot_envfile(project_dir, context: dict[str, str]):
    env_file_path = project_dir / ".env"
    env_content = (
        "DEBUG=True\n"
        f"SECRET_KEY=\"{context['secret_key']}\"\n"
        f'ALLOWED_HOSTS=\n'
        f"DATABASE_URL=sqlite:///{project_dir / 'db.sqlite3'}"
    )
    with open(env_file_path, "w") as f:
        f.write(env_content)


def create_new_project(
    *, name: str, use_lts: bool, project_dir: Path, initialize_uv: bool, initialize_env: bool
) -> dict[str, str]:
    template_context = utils.get_template_context(use_lts=use_lts)
    minor_version = template_context["docs_version"]
    template_dir_src = Path(__file__).parent / "templates" / minor_version
    shutil.copytree(template_dir_src, project_dir)
    os.rename(project_dir / "project_name", project_dir / "config")

    rename_template_files(project_dir)
    replace_variables_in_directory(
        project_dir,
        template_context,
    )
    if initialize_env is True:
        with (project_dir / "config" / "settings.py").open("r") as f:
            content = f.read()
        content = replace_settings_with_environs(content)
        with (project_dir / "config" / "settings.py").open("w") as f:
            f.write(content)
        create_dot_envfile(project_dir, template_context)

    if initialize_uv is True:
        os.chdir(project_dir)
        os.system("uv init")  # noqa: S605, S607
        os.system("rm hello.py")  # noqa: S605, S607
        os.system(f"uv add django~='{minor_version}'")  # noqa: S605
        if initialize_env is True:
            os.system("uv add environs[django]")  # noqa: S605, S607
        os.system("uv run manage.py migrate")  # noqa: S605, S607

    color.green("New Django project created.\n")

    if initialize_uv is True:
        color.green("To start Django's run server:\n")
        print(f"cd {name}")
        print("uv run manage.py runserver")

    return template_context


def handle_new(name: str, use_lts: bool, overwrite_target_dir: bool) -> None:
    if name is None:
        name = inquirer.text("Project name:").execute()

    if re.match(r"^[-a-z_]+$", name) is None:
        color.red("Invalid project name. Please use only lowercase letters, hyphens, and underscores.")
        return
    project_dir = Path.cwd() / name

    overwrite_directory_prompt(project_dir, overwrite_target_dir)

    initialize_uv = inquirer.confirm(message="Initialize your project with UV?", default=True).execute()
    initialize_env = inquirer.confirm(
        message="Initialize your project with an .env file and environs?", default=True
    ).execute()

    create_new_project(
        **{
            "name": name,
            "use_lts": use_lts,
            "project_dir": project_dir,
            "initialize_uv": initialize_uv,
            "initialize_env": initialize_env,
        }
    )
