from setuptools import setup, find_packages

setup(
    name='standwithcrypto',
    version='0.0.1',
    description='Pull US politician data from standwithcrypto.org',
    python_requires=">=3.6",
    install_requires=[
        'requests'
    ],
    packages=find_packages(exclude=['tests'])
)