# repo-to-one-file

repo-to-one-file is a Python tool that consolidates repository files into a single Markdown file. It's designed to create a comprehensive overview of a codebase, which can be particularly useful for documentation or as context for large language models.

## Features

- Generates a directory structure of the repository
- Consolidates content of specified file types (.py, .js, .ts, .json, etc.) into a single Markdown file
- Ignores common non-source files and directories (node_modules, .git, etc.)
- Configurable maximum line count per file
- Option to include normally ignored files

## Installation

You can install repo-to-one-file directly from GitHub:

```bash
pip install git+https://github.com/yourusername/repo-to-one-file.git
```
