import pathlib
import random
import shutil
import string
from unittest import TestCase

from dj_beat_drop.new import create_new_project


class TestNewCommand(TestCase):
    @staticmethod
    def _generate_random_hash(length=6):
        characters = string.ascii_lowercase + string.digits
        return "".join(random.choice(characters) for _ in range(length))  # noqa: S311

    def setUp(self):
        random_hash = self._generate_random_hash()
        self.project_name = f"test_project_{random_hash}"
        self.project_dir = pathlib.Path(__file__).parent / self.project_name
        if self.project_dir.exists():
            shutil.rmtree(self.project_dir)

    def tearDown(self):
        if self.project_dir.exists():
            shutil.rmtree(self.project_dir)

    def test_new_command_with_defaults(self):
        create_new_project(
            name=self.project_name, use_lts=True, project_dir=self.project_dir, initialize_uv=True, initialize_env=True
        )

    def test_new_command_with_no_env(self):
        create_new_project(
            name=self.project_name, use_lts=True, project_dir=self.project_dir, initialize_uv=True, initialize_env=False
        )

    def test_new_command_with_no_uv(self):
        create_new_project(
            name=self.project_name, use_lts=True, project_dir=self.project_dir, initialize_uv=False, initialize_env=True
        )

    def test_new_command_with_no_uv_and_no_env(self):
        create_new_project(
            name=self.project_name,
            use_lts=True,
            project_dir=self.project_dir,
            initialize_uv=False,
            initialize_env=False,
        )
