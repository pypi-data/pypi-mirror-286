from setuptools import find_packages, setup


def sqlglotrs_version():
    with open("sqlglotrs/Cargo.toml") as fd:
        for line in fd.readlines():
            if line.strip().startswith("version"):
                return line.split("=")[1].strip().strip('"')
    raise ValueError("Could not find version in Cargo.toml")


def get_version():
    with open("sqlglot/version.py") as fd:
        for line in fd.readlines():
            if line.strip().startswith("__version__"):
                return line.split("=")[1].strip().strip('"')
    raise ValueError("Could not find __version__ in version.py")


setup(
    name="sqlglot-doris",
    version=f"{get_version()}",
    description="An easily customizable SQL parser and transpiler",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tobymao/sqlglot",
    author="Toby Mao",
    author_email="toby.mao@gmail.com",
    license="MIT",
    packages=find_packages(include=["sqlglot", "sqlglot.*"]),
    package_data={"sqlglot": ["py.typed"]},
    # use_scm_version={
    #     "write_to": "sqlglot/_version.py",
    #     "fallback_version": "0.0.0",
    #     "local_scheme": "no-local-version",
    # },
    setup_requires=["setuptools_scm"],
    python_requires=">=3.7",
    extras_require={
        "dev": [
            "duckdb>=0.6",
            "mypy",
            "pandas",
            "pandas-stubs",
            "python-dateutil",
            "pdoc",
            "pre-commit",
            "ruff==0.4.3",
            "types-python-dateutil",
            "typing_extensions",
            "maturin>=1.4,<2.0",
        ],
        "rs": [f"sqlglotrs=={sqlglotrs_version()}"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: SQL",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
