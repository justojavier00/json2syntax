import setuptools
from setuptools import setup

setup(
    name="json_2_syntax",
    install_requires=[
        "pydantic",
    ],
    package_dir={"": "src"},
    packages = setuptools.find_packages(
        where='src',
    ),
)