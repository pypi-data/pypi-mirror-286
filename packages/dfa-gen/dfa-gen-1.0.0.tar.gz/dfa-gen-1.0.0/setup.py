# setup.py

from setuptools import setup, find_packages

setup(
    name="dfa-gen",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "graphviz"
    ],
    include_package_data=True,
    package_data={
        'dfa_gen': ['data/*.txt', 'data/*.tsv'],
    },
    entry_points={
        "console_scripts": [
            "dfa-gen=dfa_gen.generate_dfa:main",
        ],
    },
)
