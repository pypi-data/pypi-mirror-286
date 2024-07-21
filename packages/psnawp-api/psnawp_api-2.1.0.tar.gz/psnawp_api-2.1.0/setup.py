# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="psnawp_api",
    version="2.1.0",
    author="isFakeAccount",
    author_email='trevorphillips@gmx.us',
    url="https://pypi.org/project/PSNAWP/",
    homepage="https://github.com/isFakeAccount/psnawp",
    repository="https://github.com/isFakeAccount/psnawp",
    documentation="https://psnawp.readthedocs.io/en/latest/",
    keywords=["PSN", "PlayStation"],
    description="Python API Wrapper for PlayStation Network API",
    long_description="""Use `PSNAWP <https://pypi.python.org/pypi/PSNAWP>`_ instead.""",
    license="MIT",
    install_requires=['PSNAWP==2.1.0'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
