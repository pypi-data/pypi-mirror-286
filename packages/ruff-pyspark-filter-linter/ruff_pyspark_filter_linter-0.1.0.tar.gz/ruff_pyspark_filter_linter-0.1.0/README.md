# Ruff PySpark Filter Linter

This package provides a custom Ruff linter to ensure that all PySpark DataFrame instances include specified filters.

## Installation

```bash
pip install ruff_pyspark_filter_linter
````

## Usage
1. Create a ruff_pyspark_filter_linter.json configuration file with the required filters:
```json
{
  "required_filters": ["account_id", "user_id", "session_id"]
}

```

2. Running the linter on your Python files:

```bash
ruff-pyspark-filter-linter path/to/your_code.py
```

The linter will print warnings and generate a README_Rust_YYYYMMDDHHMMSS.md file with details of any missing filters.

## Building the Package

Build the source and wheel distributions.

```bash
python setup.py sdist bdist_wheel
```

## Upload to PyPI
twine upload dist/*
