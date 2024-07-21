from setuptools import setup, find_packages

setup(
    name="ruff_pyspark_filter_linter",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["ruff", "astunparse"],
    entry_points={
        "console_scripts": [
            "ruff-pyspark-filter-linter=ruff_pyspark_filter_linter.linter:lint_files"
        ],
    },
    author="Dhimahi Vavk",
    author_email="",
    description="Custom Ruff linter to ensure specific filters in PySpark DataFrame creation",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/dhimahi-vavk-fusion/ruff_pyspark_filter_linter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
