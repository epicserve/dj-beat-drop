set dotenv-load := true

_success message:
    @echo "\033[0;32m{{ message }}\033[0m"

format:
    ruff format

build:
    uv build

publish: build
    uv publish --token $PYPI_TOKEN

@update_templates:
    uv run python scripts/update_templates.py
    just _success "Templates updated."

@version_bump version:
    sed -i '' 's/version = ".*"/version = "{{ version }}"/' pyproject.toml
    uv sync
    git add pyproject.toml uv.lock
    git commit -m "Version bump to v{{ version }}"
    just _success "Version bumped to v{{ version }}."
