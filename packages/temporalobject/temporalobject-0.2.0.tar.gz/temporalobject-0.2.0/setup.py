# setup.py
from setuptools import setup, find_packages

setup(
    name="temporalobject",
    version="0.2.0",
    author="Chris Mangum",
    author_email="csmangum@gmail.com",
    description="A custom python object for storing and managing states in a temporal sequence.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/temporalobject/",
    packages=find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
