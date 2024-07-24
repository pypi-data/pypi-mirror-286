# setup.py
from setuptools import setup, find_packages

setup(
    name='ollama_api',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='HinxVietti',
    author_email='hinxvietti@gmail.com',
    description='A Python client for the Ollama API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/HinxVietti/ollama_api',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
