set dotenv-load := true

@_default:
    just --list

@_success message:
    echo "\033[0;32m{{ message }}\033[0m"

@_start_command message:
    just _success "\n{{ message }} ..."

format: format_just format_python

@format_just:
    just _start_command "Formatting Justfile"
    just --fmt --unstable

@format_python:
    just _start_command "Formatting Python"
    uv run ruff format

@lint: lint_python

@lint_python:
    just _start_command "Linting Python"
    uv run ruff check

@pre_commit: format lint test

@test:
    uv run pytest

@test_with_coverage:
    uv run pytest --cov --cov-config=pyproject.toml --cov-report=html
    open htmlcov/index.html

@update_templates:
    uv run python scripts/update_templates.py
    just _success "Templates updated."

@version_bump version:
    sed -i '' 's/version = ".*"/version = "{{ version }}"/' pyproject.toml
    uv sync
    git add pyproject.toml uv.lock
    git commit -m "Version bump to v{{ version }}"
    just _success "Version bumped to v{{ version }}."
