"""setup.py.

This setup.py file is included to support editable installations using pip's `-e`
option. The primary project configuration is specified in the pyproject.toml file. This
setup.py is only used for development installations and ensures compatibility with tools
and workflows that rely on setup.py.
"""

from setuptools import setup, find_packages

setup(
    name="chromo_map",
    version="0.1.9",  # Update this version number before releasing a new version
    description="A Python package for manipulating color maps.",
    author="Sean Smith",
    author_email="pirsquared.pirr@gmail.com",
    url="https://github.com/pirsquared/chromo-map",
    packages=find_packages(),
    include_package_data=True,
    package_data={"chromo_map": ["data/*.json"]},
    install_requires=[
        "numpy",
        "plotly",
        "matplotlib",
        "pirrtools>=0.2.10",
        "palettable",
        "svgwrite",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "build",
            "twine",
            "black",
            "pre-commit",
            "pylint",
            "sphinx",
            "sphinx-rtd-theme",
            "sphinx-copybutton",
            "sphinx-autobuild",
            "sphinx-autodoc-typehints",
            "ipython",
        ],
    },
)
