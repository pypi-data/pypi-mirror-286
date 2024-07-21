![PyPI - Python Version](https://img.shields.io/pypi/pyversions/e-lims-d2xx)
![CI](https://github.com/FabienMeyer/e-lims-d2xx/actions/workflows/ci.yml/badge.svg)
![Codecov](https://img.shields.io/codecov/c/github/FabienMeyer/e-lims-d2xx)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=FabienMeyer_e-lims-d2xx&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=FabienMeyer_e-lims-d2xx)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=FabienMeyer_e-lims-d2xx&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=FabienMeyer_e-lims-d2xx)
![PyPI](https://img.shields.io/pypi/v/e-lims-d2xx.svg)
[![Documentation](https://img.shields.io/badge/GitHub-Pages-blue)](https://fabienmeyer.github.io/e-lims-d2xx/)
![License](https://img.shields.io/github/license/FabienMeyer/e-lims-d2xx)

A brief description of what e-lims-d2xx does.

# Installation

## Install Python 3.12
If you haven’t installed Python 3.12 yet, you can download it from the [official Python website](https://www.python.org/downloads/).

## Install Poetry
If you haven’t installed Poetry yet, you can do so by following the [official Poetry installation guide](https://python-poetry.org/docs/#installation).

## Clone
Clone the repository to your local machine using.

``` bash
git clone https://github.com/FabienMeyer/e-lims-d2xx.git
cd e-lims-d2xx
```

## Configure Poetry
Configure Poetry to use a specific Python version and create a virtual environment in the project directory.
   
   ``` bash
   poetry env use "path to python 3.11 or 3.12"
   poetry config virtualenvs.in-project true
   ```

## Install dependencies
Navigate to the project directory and install the necessary dependencies using Poetry.

``` bash
poetry install
```

## Optional dependencies
If you are planning to write documentation, run quality checks, or run tests, you may need to install additional dependencies. You can do so by running.

``` bash
poetry install --with dev,doc,tests
```

## Activate the virtual environment

``` bash
      poetry shell
```