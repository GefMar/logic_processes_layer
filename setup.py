from setuptools import find_packages, setup

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="logic_processes_layer",
    version="1.1",
    description="Abstractions for create business logic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GefMar/logic_layer",
    author="Sergei (Gefest) Romanchuk",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8+",
    ],
)
