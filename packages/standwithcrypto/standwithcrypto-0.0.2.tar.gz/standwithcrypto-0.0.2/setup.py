from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='standwithcrypto',
    version='0.0.2',
    description='Pull US politician data from standwithcrypto.org',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.6",
    install_requires=[
        'requests'
    ],
    packages=find_packages(exclude=['tests'])
)