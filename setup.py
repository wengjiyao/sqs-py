# To use a consistent encoding
from codecs import open
from pathlib import Path
from setuptools import setup, find_packages

import sqs_py.about as about


here = Path.cwd()
readme = here / "README.md"

# Get the long description from the README file
with readme.open() as f:
    long_description = f.read()


setup(
    name=about.NAME,
    version=about.VERSION,
    description="AWS SQS utility package for producing and consuming messages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wengjiyao/sqs_py",
    author=about.AUTHOR.get("name"),
    author_email=about.AUTHOR.get("email"),
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
    packages=find_packages(),
    install_requires=["boto3"],
)
