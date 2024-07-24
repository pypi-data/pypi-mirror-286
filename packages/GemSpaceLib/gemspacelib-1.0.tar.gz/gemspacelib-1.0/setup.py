# setup.py

from setuptools import setup, find_packages

setup(
    name="GemSpaceLib",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "rich",
    ],
    description="A library for interacting with Gem APIs.",
    long_description="""\
    This library was programmed by Team AK:
     - Vermouth 
     - Maggie 
     - SFAH 
     - Kratos 
     - Miso 
     - Extra 
     - Serat 
     - Daisuke
     - Fenello 
     - Francis
     - Pirate - 8r9 ...
    """,
    long_description_content_type="text/plain",
    author="Vermouth",
    author_email="ver7mouth4@gmail.com",
    url="https://github.com/Vermouth4/GemSpaceLib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)