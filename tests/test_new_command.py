import random
import re
import shutil
import string
from pathlib import Path
from unittest import TestCase

from dj_beat_drop.new import create_new_project

ENV_SECRET_KEY_PATTERN = 'SECRET_KEY = env.str("SECRET_KEY")'  # noqa: S105
FILE_ASSERTIONS = {
    "manage.py": [
        "os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ project_name }}.settings')",
    ],
    "config/asgi.py": [
        "ASGI config for {{ project_name }} project.",
        "/{{ docs_version }}/howto/deployment/asgi/",
        "os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ project_name }}.settings')",
    ],
    "config/settings.py": [
        "Django settings for {{ project_name }} project.",
        "/en/{{ docs_version }}/topics/settings/",
        "/en/{{ docs_version }}/howto/deployment/checklist/",
        "SECRET_KEY = '{{ secret_key }}'",
        "ROOT_URLCONF = '{{ project_name }}.urls'",
        "WSGI_APPLICATION = '{{ project_name }}.wsgi.application'",
    ],
    "config/urls.py": [
        "/en/{{ docs_version }}/topics/http/urls/",
    ],
    "config/wsgi.py": [
        "/en/{{ docs_version }}/howto/deployment/wsgi/",
        "os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ project_name }}.settings')",
    ],
}
UV_ASSERTIONS = {
    ".python-version": [],
    "pyproject.toml": [
        'name = "{{ project_dir_name }}"',
        "django~={{ docs_version }}",
    ],
    "README.md": [],
}
ENV_ASSERTIONS = {
    ".env": [
        "DEBUG=True",
        'SECRET_KEY="{{ secret_key }}"',
        "ALLOWED_HOSTS=",
        "DATABASE_URL=sqlite:///{{ project_dir }}/db.sqlite3",
    ],
    "config/settings.py": [
        "from environs import Env",
        ENV_SECRET_KEY_PATTERN,
        'DEBUG = env.bool("DEBUG")',
        'ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")',
        'DATABASES = {"default": env.dj_db_url("DATABASE_URL")}',
    ],
}


class SafeDict(dict):
    def __missing__(self, key):
        """Make sure to keep the original placeholder if the key is missing."""
        return f"{{{key}}}"


class TestNewCommand(TestCase):
    @staticmethod
    def _generate_random_hash(length=6):
        characters = string.ascii_lowercase + string.digits
        return "".join(random.choice(characters) for _ in range(length))  # noqa: S311

    def setUp(self):
        random_hash = self._generate_random_hash()
        self.project_name = f"test_project_{random_hash}"
        self.project_dir = Path(__file__).parent.parent / self.project_name
        self.new_project_kwargs: dict[str, str | dict | bool | Path] = {
            "name": self.project_name,
            "use_lts": True,
            "project_dir": self.project_dir,
            "initialize_uv": True,
            "initialize_env": True,
        }
        if self.project_dir.exists():
            shutil.rmtree(self.project_dir)

    def tearDown(self):
        if self.project_dir.exists():
            shutil.rmtree(self.project_dir)

    @staticmethod
    def assert_files_are_correct(
        *,
        name: str,
        use_lts: bool,
        project_dir: Path,
        initialize_uv: bool,
        initialize_env: bool,
        template_context: dict,
    ):
        assertion_context = template_context.copy()
        assertion_context["project_dir_name"] = project_dir.name.replace("_", "-")
        assertion_context["project_dir"] = str(project_dir)
        for file in project_dir.rglob("*"):
            relative_path = str(file.relative_to(project_dir))
            assertions = []
            if relative_path in FILE_ASSERTIONS or relative_path in UV_ASSERTIONS or relative_path in ENV_ASSERTIONS:
                assertions.extend(FILE_ASSERTIONS.get(relative_path, []))
                uv_assertions = UV_ASSERTIONS.get(relative_path, [])
                env_assertions = ENV_ASSERTIONS.get(relative_path, [])
                if initialize_uv is True:
                    assertions.extend(uv_assertions)
                if initialize_env is True:
                    assertions.extend(env_assertions)
                with open(file) as f:
                    content = f.read()
                for assertion_pattern in assertions:
                    if (
                        assertion_pattern.startswith("SECRET_KEY =")
                        and initialize_env is True
                        and relative_path == "config/settings.py"
                    ):
                        assertion_pattern = ENV_SECRET_KEY_PATTERN
                    if re.match(r".*{{\s[_a-z]+\s}}.*", assertion_pattern) is None:
                        assertion = assertion_pattern
                    else:
                        formatted_assertion = assertion_pattern.replace("{{ ", "{").replace(" }}", "}")
                        assertion = formatted_assertion.format_map(SafeDict(assertion_context))
                    assert assertion in content, f"Assertion failed for {relative_path}: {assertion}"

    def test_new_command_with_defaults(self):
        kwargs = self.new_project_kwargs.copy()
        template_context = create_new_project(**kwargs)
        kwargs["template_context"] = template_context
        self.assert_files_are_correct(**kwargs)

    def test_new_command_with_no_env(self):
        kwargs = self.new_project_kwargs.copy()
        kwargs["initialize_env"] = False
        template_context = create_new_project(**kwargs)
        kwargs["template_context"] = template_context
        self.assert_files_are_correct(**kwargs)

    def test_new_command_with_no_uv(self):
        kwargs = self.new_project_kwargs.copy()
        kwargs["initialize_uv"] = False
        template_context = create_new_project(**kwargs)
        kwargs["template_context"] = template_context
        self.assert_files_are_correct(**kwargs)

    def test_new_command_with_no_uv_and_no_env(self):
        kwargs = self.new_project_kwargs.copy()
        kwargs["initialize_uv"] = False
        kwargs["initialize_env"] = False
        template_context = create_new_project(**kwargs)
        kwargs["template_context"] = template_context
        self.assert_files_are_correct(**kwargs)

    def test_new_command_with_defaults_and_latest_dj(self):
        kwargs = self.new_project_kwargs.copy()
        kwargs["use_lts"] = False
        template_context = create_new_project(**kwargs)
        kwargs["template_context"] = template_context
        self.assert_files_are_correct(**kwargs)

    def test_new_command_with_no_env_and_latest_dj(self):
        kwargs = self.new_project_kwargs.copy()
        kwargs["use_lts"] = False
        kwargs["initialize_env"] = False
        template_context = create_new_project(**kwargs)
        kwargs["template_context"] = template_context
        self.assert_files_are_correct(**kwargs)

    def test_new_command_with_no_uv_and_latest_dj(self):
        kwargs = self.new_project_kwargs.copy()
        kwargs["use_lts"] = False
        kwargs["initialize_uv"] = False
        template_context = create_new_project(**kwargs)
        kwargs["template_context"] = template_context
        self.assert_files_are_correct(**kwargs)

    def test_new_command_with_no_uv_and_no_env_and_latest_dj(self):
        kwargs = self.new_project_kwargs.copy()
        kwargs["use_lts"] = False
        kwargs["initialize_uv"] = False
        kwargs["initialize_env"] = False
        template_context = create_new_project(**kwargs)
        kwargs["template_context"] = template_context
        self.assert_files_are_correct(**kwargs)
