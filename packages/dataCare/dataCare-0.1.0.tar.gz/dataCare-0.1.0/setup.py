# setup.py

from setuptools import setup, find_packages

setup(
    name='dataCare',
    version='0.1.0',
    description='A library for automated data cleaning, preprocessing, labeling, and privacy.',
    author='Keshav',
    author_email='keshgarg24@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scikit-learn',
        'cryptography',
        'pytest'
    ],
    test_suite='tests',
)
