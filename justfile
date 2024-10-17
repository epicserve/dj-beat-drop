set dotenv-load := true

@_success message:
    echo "\033[0;32m{{ message }}\033[0m"

@_start_command message:
    just _success "\n{{ message }} ..."

build:
    rm -rf dist/
    uv build
format: format_just format_python

@format_just:
    just _start_command "Formatting Justfile"
    ruff format

@format_python:
    just _start_command "Formatting Python"
    ruff format

publish: build
    uv publish --token $PYPI_TOKEN

@test:
    uv run pytest

@update_templates:
    uv run python scripts/update_templates.py
    just _success "Templates updated."

@version_bump version:
    sed -i '' 's/version = ".*"/version = "{{ version }}"/' pyproject.toml
    uv sync
    git add pyproject.toml uv.lock
    git commit -m "Version bump to v{{ version }}"
    just _success "Version bumped to v{{ version }}."

