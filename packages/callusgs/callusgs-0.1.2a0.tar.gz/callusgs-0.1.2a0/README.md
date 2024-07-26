# callusgs

Implementation of USGS's machine-to-machine API 

## Features

`callusgs` is both a python package and a suite of command line tools.

## Installation

### Prerequisites

- account at USGS
- access to m2m MACHINE, otherwise: see resticions

Install the package together with the respective command line applications from pip.

```bash
pip install callusgs
```

## Usage

For more detailed usage instructions and/or examples, please refer to the documentation linked below.

### Command Line Tools

#### Download

```bash
callusgs download
```

#### Geocode

```bash
callusgs geocode
```

#### Grid2ll

```bash
callusgs grid2ll
```

## Documentation

See the docs folder for raw documentation or visit [callusgs.readthedocs.io](https://callusgs.readthedocs.io).

## License

- `callusgs` is licensed under the [GPL-v2](LICENSE)
- the file `docs/requirements.txt` is licensed under the MIT license.

## Citation

If you use this software, please use the bibtex entry below or refer to [the citation file](CITATION.cff).

```
@software{callusgs,
author = {Katerndahl, Florian},
license = {GPL-2.0},
title = {{callusgs}},
url = {https://github.com/Florian-Katerndahl/callusgs}
}
```

## Acknowledgments

- Most of the docstrings were provided by the USGS in their API documentation.  
- The download application took initial inspiration from [the example script provided by the USGS](https://m2m.cr.usgs.gov/api/docs/example/download_data-py).
- `docs/requirements.txt` is taken from [here](https://docs.readthedocs.io/en/stable/guides/reproducible-builds.html)
