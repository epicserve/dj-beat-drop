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
