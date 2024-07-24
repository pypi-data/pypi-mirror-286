# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['stories', 'stories.steps']

package_data = \
{'': ['*']}

install_requires = \
['anndata>=0.10.7,<0.11.0',
 'cellrank>=2.0.4,<3.0.0',
 'flax>=0.8.2,<0.9.0',
 'jax>=0.4.25,<0.5.0',
 'jaxlib>=0.4.25,<0.5.0',
 'jaxopt>=0.8.3,<0.9.0',
 'numpy>=1.26.4,<2.0.0',
 'optax>=0.2.2,<0.3.0',
 'orbax-checkpoint>=0.5.20,<0.6.0',
 'ott-jax>=0.4.5,<0.5.0',
 'scikit-learn>=1.5.1,<2.0.0',
 'seaborn>=0.13.2,<0.14.0',
 'tqdm>=4.66.2,<5.0.0']

setup_kwargs = {
    'name': 'stories-jax',
    'version': '0.1.0',
    'description': 'Learn spatially informed Waddington-like potentials for single-cell gene expression',
    'long_description': '# Learning cell fate landscapes from spatial transcriptomics using Fused Gromov-Wasserstein\n\n[![codecov](https://codecov.io/gh/gjhuizing/stories/graph/badge.svg?token=5DWDYPAUYI)](https://codecov.io/gh/gjhuizing/stories)\n[![Tests](https://github.com/cantinilab/stories/actions/workflows/main.yml/badge.svg)](https://github.com/cantinilab/stories/actions/workflows/main.yml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nSTORIES is a novel trajectory inference method for spatial transcriptomics data profiled at several time points, relying on Wasserstein gradient flow learning and Fused Gromov-Wasserstein. [Read the preprint here](https://www.biorxiv.org/content/xxxxx) and [the documentation here](https://stories.rtfd.io)!\n\n![introductory figure](docs/_static/fig1.png)\n\n## Install the package\n\nSTORIES is implemented as a Python package seamlessly integrated within the scverse ecosystem. It relies on JAX for fast GPU computations and JIT compilation, and OTT for Optimal Transport computations.\n\n### via PyPI (recommended)\n\n```bash\npip install stories-jax\n```\n\n### via GitHub (development version)\n\n```bash\ngit clone git@github.com:cantinilab/stories.git\npip install ./stories/\n```\n\n## Getting started\n\nSTORIES takes as an input an AnnData object, where omics information and spatial coordinates are stored in `obsm`, and `obs` contains time information, and optionally a proliferation weight. Visit the **Getting started** and **API** sections for tutorials and documentation.\n',
    'author': 'Geert-Jan Huizing',
    'author_email': 'gjhuizing@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
