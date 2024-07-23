"""Python setup.py for streamauc package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("streamauc", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="streamauc",
    version=read("streamauc", "VERSION"),
    description="Stream and minibatch based metrics for probabilistic "
                "multi-class classification.",
    url="https://github.com/FabricioArendTorres/streamAUC/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Fabricio Arend Torres",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=["numpy", "matplotlib", "numba"],
    extras_require={"test": ["pytest", "coverage", "flake8", "black",
                             "isort", "pytest-cov", "mypy", "gitchangelog",
                             "pdoc3", "scikit-learn", "ipdb", "tqdm"]},
)
