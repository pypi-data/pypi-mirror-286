# setup.py
from setuptools import setup, find_packages

setup(
    name="TaskFormatter",
    version="1.0.0",
    description="A Python package for function execution status and spinner output",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Sean Smith",
    author_email="sean@ssmith.app",
    url="https://github.com/seanssmith/TaskFormatter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
