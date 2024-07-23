# setup.py

from setuptools import setup, find_packages

setup(
    name="mypackage-fenglv",
    version="0.1.0",
    author="leon feng",
    author_email="leon.feng@nio.com",
    description="A simple example package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://ad-gitlab.nioint.com/leon.feng/mypackage",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy>=1.21.0",
        "pandas==1.3.0",
        "scipy>=1.5.0,<2.0.0"
    ],
    test_suite='tests',
)
