from setuptools import setup, find_packages
import os

VERSION = '0.0.2'
DESCRIPTION = 'Generate Reddit Text-to-Speech videos'
from pathlib import Path
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

# Setting up
setup(
    name="autovid",
    version=VERSION,
    author="Ajinkya Talekar",
    author_email="ajinkyat@buffalo.edu",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['selenium', 'moviepy', 'gtts', 'praw'],
    keywords=['python', 'reddit', 'tts', 'video generator', 'automation'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)