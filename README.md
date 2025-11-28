1. install pipx https://github.com/pypa/pipx
2. install poetry https://python-poetry.org/docs/
3. run `poetry run mkdocs serve` to start a local server

## How to install new plugins

Use the `poetry` tool to manage dependencies and install new plugins.:
```bash
poetry add -D <plugin-package-name>
```

For example:
```bash
poetry add -Dmkdocs-redirects     
```