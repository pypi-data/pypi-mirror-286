# Stack Generator

A CLI tool to generate a code base from any cookiecutter template

## Installation

```bash
pip install stack-gen
```

## CLI Usage

```bash
sg [OPTIONS] [ARGS]...

Options:
  -r,   --repository TEXT        Name of github repository containing the template to generate
  -u    --user TEXT              Name of github's user owning the repository
  -gac  --access_token TEXT      Write GITHUB_ACCESS_TOKEN env variable into .env file (Optional)

  --help                         Show this message and exit.
```

## Example

To clone [this](https://github.com/hourlier96/fastapi-generator) cookiecutter template:

```bash
sg -r fastapi-generator -u hourlier96
```

## Informations

Specified repository MUST respect [cookiecutter template format](https://cookiecutter.readthedocs.io/en/stable/overview.html).

Specified user MUST owned the repository specified.

## License

[MIT](https://choosealicense.com/licenses/mit/)
