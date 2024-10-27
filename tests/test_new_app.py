import re
import shutil
from pathlib import Path

from dj_beat_drop.new_app import create_new_app
from tests.base_test import BaseTest, SafeDict

FILE_ASSERTIONS = {
    "migrations/__init__.py": [],
    "__init__.py": [],
    "admin.py": [
        "from django.contrib import admin",
    ],
    "apps.py": [
        "class {{ camel_case_app_name }}Config(AppConfig):",
        "default_auto_field = 'django.db.models.BigAutoField'",
        "name = '{{ app_name }}'",
    ],
    "models.py": [
        "from django.db import models",
    ],
    "tests.py": [
        "from django.test import TestCase",
    ],
    "views.py": [
        "from django.shortcuts import render",
    ],
}


class TestNewAppCommand(BaseTest):
    app_dir: Path

    def remove_app_dir(self):
        if self.app_dir.exists():
            shutil.rmtree(self.app_dir)

    def _setup_app_dir(self, app_rel_path: str):
        self.app_dir = Path(__file__).parent / app_rel_path
        self.addCleanup(self.remove_app_dir)
        self.remove_app_dir()

    @staticmethod
    def assert_files_are_correct(
        *,
        template_context: dict[str, str],
        app_dir: Path,
    ):
        assertion_context = template_context.copy()
        for file in app_dir.rglob("*"):
            relative_path = str(file.relative_to(app_dir))
            assertions = []
            if relative_path in FILE_ASSERTIONS:
                assertions.extend(FILE_ASSERTIONS.get(relative_path, []))
                assert file.exists() is True, f"File does not exist: {file}"
                with file.open("r") as f:
                    content = f.read()
                for assertion_pattern in assertions:
                    if re.match(r".*{{\s[_a-z]+\s}}.*", assertion_pattern) is None:
                        assertion = assertion_pattern
                    else:
                        formatted_assertion = assertion_pattern.replace("{{ ", "{").replace(" }}", "}")
                        assertion = formatted_assertion.format_map(SafeDict(assertion_context))
                    assert assertion in content, f"Assertion failed for {relative_path}: {assertion}"

    def test_new_app_with_sub_dir(self):
        app_rel_path = "apps/accounts"
        self._setup_app_dir(app_rel_path)
        kwargs = {}
        kwargs["template_context"] = create_new_app(app_rel_path)
        kwargs["app_dir"] = self.app_dir
        self.assert_files_are_correct(**kwargs)

    def test_new_app_with_same_dir(self):
        app_rel_path = "accounts"
        self._setup_app_dir(app_rel_path)
        kwargs = {}
        kwargs["template_context"] = create_new_app(app_rel_path)
        kwargs["app_dir"] = self.app_dir
        self.assert_files_are_correct(**kwargs)
