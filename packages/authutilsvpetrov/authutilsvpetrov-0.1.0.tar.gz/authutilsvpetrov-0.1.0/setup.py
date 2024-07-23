"""
Setup file for auth_utils package
"""
from setuptools import setup, find_packages

setup(
    name='authutilsvpetrov',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'pydantic',
        'typing',
        'userutilsvpetrov'
    ]
)
