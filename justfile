set dotenv-load := true

format:
    ruff format

build:
    uv build

publish: build
    uv publish --token $PYPI_TOKEN
