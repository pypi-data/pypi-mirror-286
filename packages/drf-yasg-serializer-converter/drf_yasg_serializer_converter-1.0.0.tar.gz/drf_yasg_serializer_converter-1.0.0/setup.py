from setuptools import setup, find_packages
import codecs
import os

from src.drf_yasg_serializer_converter.default_values import SERIALIZER_CONVERTOR_VERSION

here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, "src/README.md")
if os.path.isfile(readme_path):
    with codecs.open(readme_path, encoding="utf-8") as fh:
        long_description = "\n" + fh.read()
else:
    long_description = "\n"

VERSION = SERIALIZER_CONVERTOR_VERSION
print(f'App version: {VERSION}')
DESCRIPTION = 'Converts django serializer to drf_yasg openapi schema.'

# Setting up
setup(
    name="drf_yasg_serializer_converter",
    version=VERSION,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    author="Greewil (Shishkin Sergey)",
    author_email="shishkin.sergey.d@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/Greewil/drf-yasg-serializer-converter",
    install_requires=['Django', 'drf-yasg'],
    keywords=['python', 'openapi schema generation', 'django serializer convertor'],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.10"
)

# https://pypi.org/classifiers/

# # Usage:
# pip install wheel
# python setup.py bdist_wheel sdist
# twine check dist/*
# twine upload -r testpypi dist/*
# twine upload dist/*
