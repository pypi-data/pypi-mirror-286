# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crispr_ambiguous_mapping',
 'crispr_ambiguous_mapping.mapping',
 'crispr_ambiguous_mapping.models',
 'crispr_ambiguous_mapping.parsing',
 'crispr_ambiguous_mapping.processing',
 'crispr_ambiguous_mapping.quality_control',
 'crispr_ambiguous_mapping.utility',
 'crispr_ambiguous_mapping.visualization']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.81,<2.0',
 'matplotlib==3.9.0',
 'numpy>=1.24.4,<2.0.0',
 'pandarallel>=1.6.4,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'scipy>=1.10.1,<2.0.0',
 'seaborn==0.13.2',
 'typeguard>=3.0.2,<4.0.0']

setup_kwargs = {
    'name': 'crispr-ambiguous-mapping',
    'version': '0.0.160',
    'description': '',
    'long_description': '',
    'author': 'Basheer Becerra',
    'author_email': 'bbecerr@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
