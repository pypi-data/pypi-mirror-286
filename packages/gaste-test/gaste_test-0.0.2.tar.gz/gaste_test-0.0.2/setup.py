"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

import pathlib

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# This call to setup() does all the work
setup(
    name="gaste_test",
    version="0.0.2",
    description="Gamma approximation of stratified truncated exact test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alexandre WENDLING",
    author_email="alexandre.wendling@univ-grenoble-alpes.fr",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=["numpy", "pandas", "scipy", "matplotlib", "tqdm"],
    extras_require={
        "dev": [
            "black",
            "flake8",
            "isort",
            "sphinx",
            "sphinx_rtd_theme",
            "setuptools",
            "wheel",
            "twine",
        ]
    },
)
