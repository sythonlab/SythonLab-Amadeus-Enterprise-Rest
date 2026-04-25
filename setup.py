from setuptools import setup, find_packages

setup(
    name="sythonlab_amadeus_enterprise_rest",
    version="0.0.6",
    packages=find_packages(),
    install_requires=[],
    url="https://github.com/sythonlab/SythonLab-Amadeus-Enterprise-Rest",
    author="José Angel Alvarez Abraira",
    author_email="sythonlab@gmail.com",
    description="Sython Lab Amadeus Enterprise REST API Client",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
