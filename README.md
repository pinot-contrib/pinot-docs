# Apache Pinot Documentation

This repository contains the source code for the Apache Pinot documentation site.
Originally this doc was built using GitBook, but we are migrating to MkDocs with Material for MkDocs theme.

Feel free to read [copilot-instructions.md](.github/copilot-instructions.md) and [doc-style.md](doc-style.md) for more 
information about contributing to the documentation.

## How to run the documentation site locally

1. install pipx https://github.com/pypa/pipx
2. install poetry https://python-poetry.org/docs/
3. run the following to start a local server

```bash
`poetry run mkdocs serve --livereload`
```

## How to install new plugins

Use the `poetry` tool to manage dependencies and install new plugins.:
```bash
poetry add -D <plugin-package-name>
```

For example:
```bash
poetry add -Dmkdocs-redirects     
```