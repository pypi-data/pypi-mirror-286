"""
Setup file for auth_utils package
"""
from setuptools import setup, find_packages

setup(
    name="authutilsvpetrov",
    version="0.1.6",
    author="Vladimir Petrov",
    author_email="",
    description="description",
    long_description="longdescription",
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "fastapi",
        "pydantic",
        "typing",
        "user-utils-vpetrov"
    ],
)
