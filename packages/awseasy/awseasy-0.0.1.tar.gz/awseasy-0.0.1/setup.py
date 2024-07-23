# setup.py

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="awseasy",
    version="0.0.1",
    author="Byoungkwon An",
    author_email="drancom@gmail.com",
    description="A package to simplify AWS usage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    install_requires=[
        'boto3',
        'python-dotenv',
    ],
)