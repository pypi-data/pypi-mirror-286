# Author: HAKOISHI Kenta <hakoken.of.joytoy@gmail.com>
# Copyright (c) 2024- HAKOISHI Kenta
# Licence: MIT

from setuptools import setup

DESCRIPTION = 'Generate a hydrograph and a hyetograph.'
NAME = 'hydrohyeto-matplotlib'
AUTHOR = 'HAKOISHI Kenta'
AUTHOR_EMAIL = 'hakoken.of.joytoy@gmail.com'
URL = 'https://github.com/yakitoritabetai/hydrohyeto-matplotlib'
LICENSE = 'MIT'
DOWNLOAD_URL = URL
VERSION = '0.1.0'
PYTHON_REQUIRES = '>=3.11'
INSTALL_REQUIRES = [
    'japanize-matplotlib',
    
]
PACKAGES = [
    'hydrohyeto_matplotlib'
]
KEYWORDS = 'matplotlib'
CLASSIFIERS=[
    'License :: OSI Approved :: MIT License'
]

with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()
LONG_DESCRIPTION = readme
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url=URL,
    download_url=URL,
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
    license=LICENSE,
    keywords=KEYWORDS,
    install_requires=INSTALL_REQUIRES
)