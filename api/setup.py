"""
ACHTUNG: You *must* adapt the "install_requires", "setup_requires",
         and "tests_require" sections!
         Pin you dependencies!
         Classifiers are optional but recommended!
         I'll stop being excited now!
"""

import re

from setuptools import setup, find_packages

project_package = 'wsi_api'
project_info = {}

with open('{}/__init__.py'.format(project_package), 'r') as f:
    for _ in f.read().splitlines():
        b = re.search(r'^__(.*)__\s*=\s*[\'"]([^\'"]*)[\'"]', _)
        if b:
            project_info[b.group(1)] = b.group(2)


setup(
    name=project_info['title'],
    version=project_info['version'],
    author=project_info['author'],
    author_email=project_info['author_email'],
    url=project_info['url'],
    license=project_info['license'],
    description=project_info['description'],
    long_description=open('README.md').read(),
    packages=find_packages(),
    include_package_data=True,

    keywords='flask webapp',
    install_requires=[
        'Flask',
        'gunicorn'
    ],
    setup_requires=[
        'pytest-runner',
        'wheel',
        'Sphinx',
        'sphinx_rtd_theme',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-flake8',
        'pytest-flask',
        'pytest-watch',
    ],

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.6',
    ],
)
