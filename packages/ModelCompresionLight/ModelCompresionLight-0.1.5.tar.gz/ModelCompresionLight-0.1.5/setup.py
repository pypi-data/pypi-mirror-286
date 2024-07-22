
# Licensed under the MIT license.

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()

setup(
    name = 'ModelCompresionLight',
    version = '0.1.5',
    author = 'CO-AI-TECH Team',
    author_email = '710783785@qq.com',
    description = 'Lighter Model Ensemble for model mc',
    long_description = read('README.rst'),
    license = 'MIT',
    url = None,

	packages=find_packages('ModelCompresionLight',exclude=["*.ModelZoo"]),
	package_dir = {'':'ModelCompresionLight'},
    python_requires = '>=3.6.2',
    install_requires = [
        'thop',

    ]


)
