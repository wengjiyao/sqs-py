# To use a consistent encoding
from codecs import open
from pathlib import Path
from setuptools import setup, find_packages

import pysqs.about as about


here = Path.cwd()
readme = here / "README.md"

# Get the long description from the README file
with readme.open() as f:
    long_description = f.read()


setup(
    name=about.NAME,
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=about.VERSION,
    description="AWS SQS utility package for producing and consuming messages",
    long_description=long_description,
    # The project's main homepage.
    url="https://github.com/hjpotter92/pysqs",
    # Author details
    author=about.AUTHOR.get("name"),
    author_email=about.AUTHOR.get("email"),
    # Choose your license
    license="MIT",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.7",
    ],
    # What does your project relate to?
    keywords="aws sqs messages producer/consumer",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),
    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=["boto3"],
)
