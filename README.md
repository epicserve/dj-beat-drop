# dj-beat-drop

<img src="images/logo.jpg" alt="Logo" style="width: 250px;">

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

- **LTS Version**: Add an option so you can use the latest LTS version of Django instead of the latest release default.
- **Environment Variables**: Add support for environment variables to configure the project.
- **Tests**: Add tests to ensure the utility works as expected.
- **Third-Party Templates**: Add support for using a third-party template.
- **Polish**: Add lots of polish inspired by `laravel` CLI.
- **Additional Subcommands**: Introduce more subcommands to enhance functionality.
- **Official Django Project**: Aim to have this utility included as an official Django project, potentially renaming the 
  command to `django` for easier usage (e.g., `django new`).
- ~~**`pyproject.toml` Integration**: Set up new Django projects with a `pyproject.toml` file that can be used by `uv` to
  run the project.~~

## Installation

```sh
pip install dj-beat-drop
```

## Usage

```sh
# If you just installed dj-beat-drop, then reload your shell to make the command available.
beatdrop new example_project
```