# Getting Started

This guide explains how to set up and run the FastAPI backend using [uv](https://github.com/astral-sh/uv), a fast Python package manager.

## Prerequisites

- Docker installed, see [Install Docker](https://docs.docker.com/get-docker/)
- Python 3.13 or newer installed [Python official page](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv) installed, see [Install 'uv'](#1-install-uv)

## Environment variables

To make sure the terminal can find your python and uv executables, you need to add the paths to your environment variables.

Assuming your python.exe file located at: `C:\Users\<username>\AppData\Local\Programs\Python\Python3.13\python.exe`

You should add the following to your 'PATH' environment variable:

```bash
C:\Users\<username>\AppData\Local\Programs\Python\Python3.13
C:\Users\<username>\AppData\Local\Programs\Python\Python3.13\Scripts
```

For more help you can see the following video: [How to add Python to PATH on Windows](https://www.youtube.com/watch?v=91SGaK7_eeY)

## 1. Install `uv`

#### Using pip

```bash {"interpreter":"bash"}
python -m pip install uv
```

#### Using the installer

[uv official page](https://docs.astral.sh/uv/getting-started/installation/).

## 2. Init uv project

```bash
uv init
```

## 3. Remove the .python-version file

We would like to use the Python version specified in the `pyproject.toml` file,
so we need to remove the `.python-version` file that was created by `uv init`.

```bash
rm .python-version
```

## 4. Add dependencies

```bash
# FastAPI contains the cli and more usefull features, in case you want all, you can replace with `fastapi[all]`
uv add fastapi[standard]
```

```bash
# Pydantic is used for data validation and settings management using Python type annotations.
# It is a core dependency for FastAPI, as it provides the data models for request and response bodies.
uv add pydantic
```

```bash
# pydantic-settings is used for managing application settings and configuration using Pydantic models.
# We will use it to manage environment variables and application settings and make sure they are loaded correctly and
# type-checked.
uv add pydantic-settings
```

```bash
# python-dotenv is used to read key-value pairs from a .env file and set them as environment variables.
uv add python-dotenv
```

```bash
# SQLAlchemy is a popular ORM (Object Relational Mapper) for Python, used for database interactions.
uv add sqlalchemy
```

```bash
# Alembic is a lightweight database migration tool for usage with SQLAlchemy.
uv add alembic
```

```bash
# python-jose is used for JWT token encoding and decoding, commonly used for authentication.
# passlib provides password hashing utilities, with bcrypt as a secure hashing algorithm.
uv add python-jose[cryptography] passlib[bcrypt]
```

## 5. Add development dependencies

```bash
# Ruff is a linter and formatter for Python, useful for maintaining code quality.
uv add --dev ruff
```

```bash
# ty is a type checker for Python, useful for checking type hints and ensuring type safety (compiler like for python).
uv add --dev ty
```

```bash
# Pytest is a testing framework, useful for writing and running tests.
uv add --dev pytest pytest-pythonpath
```

```bash
# Pre-commit is a framework for managing and maintaining multi-language pre-commit hooks.
# We will use it to run linters and formatters automatically before committing code.
uv add --dev pre-commit
```

```bash
# HTTPX is an HTTP client for Python, useful for making HTTP requests and test fastAPI server.
uv add --dev httpx
```
