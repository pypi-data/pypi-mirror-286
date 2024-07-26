import re
import pathlib 
import setuptools


_here = pathlib.Path()

name = "PySauron"
author = "Bogdan Ivanyuk-Skulskyi"
description = "A collection of datasets for video anomaly detection"
python_requires = ">=3.8.0"
url = "https://github.com/KyloRen1/" + name


with open(_here / name.lower().replace('-', '_') / "__init__.py") as f:
    meta_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if meta_match:
        version = meta_match.group(1)
    else:
        raise RuntimeError("Unable to find __version__ string")

with open(_here / "README.md" , "r") as f:
    readme = f.read()


setuptools.setup(
    name=name,
    version=version,
    author=author,
    description=description,
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=python_requires,
    url=url,
    install_requires=[],
    include_package_data=True,
    license="MIT",  # Don't forget to change classifiers if you change the license
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=setuptools.find_packages(
        exclude=["test", "test*", "assets"]
    ),
)