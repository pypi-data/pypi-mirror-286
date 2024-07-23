"""
Setup file for auth_utils package
"""
from setuptools import setup, find_packages

setup(
    name='auth_utils_vpetrov',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'pydantic',
        'user_utils',
        'typing',
        'user-utils-vpetrov'
    ]
)
