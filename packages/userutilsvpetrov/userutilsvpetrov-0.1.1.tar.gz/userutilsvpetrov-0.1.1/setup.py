"""
Setup file for user_utils package
"""
from setuptools import setup, find_packages

setup(
    name='userutilsvpetrov',
    version='0.1.1',
    author="Vladimir Petrov",
    author_email="",
    description="A package for user utilities",
    long_description="This is a package that provides utilities for user management.",
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
        'fastapi',
        'pydantic',
        'sqlalchemy',
        'alembic',
        'email-validator',
        'python-dateutil'
    ]
)