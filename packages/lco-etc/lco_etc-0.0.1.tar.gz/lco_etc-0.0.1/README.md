# lco_etc

[![Template](https://img.shields.io/badge/Template-LINCC%20Frameworks%20Python%20Project%20Template-brightgreen)](https://lincc-ppt.readthedocs.io/en/latest/)
[![PyPI](https://img.shields.io/pypi/v/lco_etc?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/lco-etc/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bradengarretson/lco-etc/smoke-test.yml)](https://github.com/bradengarretson/lco-etc/actions/workflows/smoke-test.yml)
[![Codecov](https://codecov.io/gh/bradengarretson/lco-etc/branch/main/graph/badge.svg)](https://codecov.io/gh/bradengarretson/lco-etc)
[![Read The Docs](https://img.shields.io/readthedocs/lco-etc)](https://lco-etc.readthedocs.io/)
[![Benchmarks](https://img.shields.io/github/actions/workflow/status/bradengarretson/lco-etc/asv-main.yml?label=benchmarks)](https://bradengarretson.github.io/lco-etc/)

This project was automatically generated using the LINCC-Frameworks [python-project-template](https://github.com/lincc-frameworks/python-project-template).

For more information about the project template see the [documentation](https://lincc-ppt.readthedocs.io/en/latest/).

## Overview

`lco_etc` is a Python package designed to calculate exposure times for the Las Cumbres Observatory Telescopes. The original exposure time calculator was implemented as a webpage at [LCO Exposure Time Calculator](https://exposure-time-calculator.lco.global/#) and adapted to Python by rewriting the embedded JavaScript code. This Python adaptation provides a programmatic interface for calculating exposure times, making it accessible for automation and integration into other Python-based workflows.

## Installation

### Using pip

You can install the latest release of `lco_etc` from PyPI:

```bash
pip install lco_etc
```

## Usage

To use the `lco_etc` package, you can import it into your Python scripts and call the provided functions. Below is a quick example:

```python
from lco_etc.etc import exposure_time_calc

result = exposure_time_calc(10.0, 20, None, "sinistro", "V", "new", 1.2)
print(result)
```

### Output

``` python
{'snr': 10.2, 'magnitude': 20.0, 'exposure_time': 29.0, 'saturated': False, 'mag_system': 'Vega'}
```
