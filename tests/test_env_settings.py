from pathlib import Path

from dj_beat_drop.new import replace_settings_with_environs
from dj_beat_drop.utils import get_latest_django_version


def test_replace_settings_with_environs():
    _, minor_version = get_latest_django_version()
    current_dir = Path(__file__).parent.parent
    settings_file_path = current_dir.joinpath(
        f"src/dj_beat_drop/templates/{minor_version}/project_name/settings.py-tpl"
    )
    print(settings_file_path)
    with open(settings_file_path, "r") as f:
        env_settings_content = f.read()
    result = replace_settings_with_environs(env_settings_content)

    assert "from environs import Env" in result
    assert "env = Env()" in result
    assert "env.read_env()" in result
    assert 'SECRET_KEY = env.str("SECRET_KEY")' in result
    assert 'DEBUG = env.bool("DEBUG")' in result
    assert 'ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")' in result
    assert r'DATABASES = {"default": env.dj_db_url("DATABASE_URL")}' in result
