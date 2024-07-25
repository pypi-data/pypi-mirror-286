from setuptools import setup, find_packages

setup(
    name="device-format",
    version="0.1",
    packages=find_packages(),
    author="Aung Htoo Khine",
    description="This package is designed to generate regular expression formats based on device names.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
