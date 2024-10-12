# dj-beat-drop

`dj-beat-drop` is a CLI utility designed to simplify the creation of new Django projects by organizing all configuration
files into a `config` directory, instead of using Django's default naming convention. This approach avoids the
antipattern of naming the config directory the same as the project name.

## Project Status

This project is in the very early stages of development, focusing on defining the API. Future releases will include
additional features and improvements.

## Features

- **Simplified Project Structure**: All configuration files are placed in a `config` directory.
- **Latest Django Version**: Currently, the utility uses the latest release of Django.

## Future Goals

- **Specify Django Version**: Add an option to specify the Django version when creating a new project.
- **Polish**: Add lots of polish inspired by `laravel` CLI. Possibly refactor to use Rust or the coolest CLI library.
- **Additional Subcommands**: Introduce more subcommands to enhance functionality.
- **Official Django Project**: Aim to have this utility included as an official Django project, potentially renaming the 
  command to `django` for easier usage (e.g., `django new`).
- **`pyproject.toml` Integration**: Set up new Django projects with a `pyproject.toml` file that can be used by `uv` to
  run the project.

## Installation

```sh
pip install dj-beat-drop
```

## Usage

```sh
beatdrop new example_project
```