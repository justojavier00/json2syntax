import setuptools
from setuptools import setup

setup(
    name="json2syntax",
    install_requires=[
        "pydantic",
    ],
    package_dir={"": "src"},
    packages = setuptools.find_packages(
        where='src',
    ),

    entry_points={
        'console_scripts': [
            'json2syntax = json2syntax.json2syntax:json2syntax'
        ]
    }
)