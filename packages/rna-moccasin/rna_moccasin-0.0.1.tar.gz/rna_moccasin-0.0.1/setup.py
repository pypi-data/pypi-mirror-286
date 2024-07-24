from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='rna_moccasin',
    author="BioCiphers",
    author_email="admin@biociphers.org",
    version='0.0.1',
    packages=find_packages(),
    license='MIT License',
    description="dummy package for rna_moccasin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://majiq.biociphers.org/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
