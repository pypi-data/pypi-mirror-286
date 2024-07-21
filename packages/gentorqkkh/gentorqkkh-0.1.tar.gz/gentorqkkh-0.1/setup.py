from setuptools import setup, find_packages

setup(
name="gentorqkkh",
version="0.1",
description="A simple Python Json Config Package for minimal projects.",
packages=find_packages(),
requires=[
    'requests',
    'pyperclip',
],
classifiers=[
"Programming Language :: Python :: 3",
"License :: OSI Approved :: MIT License",
"Operating System :: OS Independent",
],
python_requires=">=3.6",
)