"""
Setup file for user_utils package
"""
from setuptools import setup, find_packages

setup(
    name='userutilsvpetrov',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'pydantic',
        'sqlalchemy',
        'alembic',
        'email-validator',
        'python-dateutil'
    ]
)
