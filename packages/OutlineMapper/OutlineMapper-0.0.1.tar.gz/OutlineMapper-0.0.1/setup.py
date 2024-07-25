from setuptools import setup, find_packages
from os import path
working_dir = path.abspath(path.dirname(__file__))

with open(path.join(working_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='OutlineMapper',
    version='0.0.1',
    url = 'https://github.com/RyuKaSa/OutlineMapper',
    author='Ryukasa',
    author_email='william.bogdanovic@yahoo.fr',
    description='Simple outline mapper for images, using color clustering',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pillow',
        'matplotlib',
        'scikit-learn',
        'scipy'
    ],
)