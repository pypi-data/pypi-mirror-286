"""
Setup file for auth_utils package
"""
from setuptools import setup, find_packages

setup(
    name='auth_utils_vpetrov',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'pydantic',
        'typing',
        'user-utils-vpetrov'
    ]
)
