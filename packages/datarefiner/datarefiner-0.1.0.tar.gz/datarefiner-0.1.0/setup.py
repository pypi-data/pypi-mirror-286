#!/usr/bin/env python
# Created by "Thieu" at 14:47, 25/07/2024 ----------%
#       Email: nguyenthieu2102@gmail.com            %
#       Github: https://github.com/thieu1995        %
# --------------------------------------------------%

from setuptools import setup, find_packages


def readme():
    with open('README.md', encoding='utf-8') as f:
        README = f.read()
    return README


setup(
    name="datarefiner",
    version="0.1.0",
    author="Thieu",
    author_email="nguyenthieu2102@gmail.com",
    description="DataRefiner: An Advanced Toolkit for Data Transformation and Processing",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords=["Data refining", "Data tidying", "Data munging",
              "Data grooming", "Data optimization", "Data formatting", "Data structuring"
              "Data filtering", "Data cleansing", "Data standardization", "Data enrichment", "Feature engineering",
              "Data wrangling", "Data transformation", "Data scaling", "Data normalization"
              "Data preprocessing", "Data preparation", "Data analysis",],
    url="https://github.com/thieu1995/datarefiner",
    project_urls={
        'Documentation': 'https://datarefiner.readthedocs.io/',
        'Source Code': 'https://github.com/thieu1995/datarefiner',
        'Bug Tracker': 'https://github.com/thieu1995/datarefiner/issues',
        'Change Log': 'https://github.com/thieu1995/datarefiner/blob/master/ChangeLog.md',
        'Forum': 'https://t.me/+fRVCJGuGJg1mNDg1',
    },
    packages=find_packages(exclude=['tests*', 'examples*']),
    include_package_data=True,
    license="GPLv3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Benchmark",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    install_requires=["numpy>=1.17.1", "scipy>=1.7.1", "scikit-learn>=1.0.2",
                      "pandas>=1.3.5", "permetrics>=2.0.0"],
    extras_require={
        "dev": ["pytest>=7.0", "pytest-cov==4.0.0", "flake8>=4.0.1"],
    },
    python_requires='>=3.8',
)
