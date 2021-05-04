"""
Setup to create the package
"""
import setuptools

import polidoro_argument

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='polidoro-argument',
    version=polidoro_argument.VERSION,
    description='Package to create command line arguments for Python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/heitorpolidoro/polidoro-argument',
    author='Heitor Polidoro',
    license='unlicense',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)
