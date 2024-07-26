from setuptools import setup, find_packages

# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read the contents of your requirements file
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='depmap',
    version='0.1.2',  
    description='Dependency Mapper CLI for managing and analyzing software dependencies across repositories.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='David Schwartz',
    author_email='david.schwartz@devfactory.com',
    url='https://github.com/trilogy-group/central-product-tpm/tree/master/POC/cc/repo/depmap/cli',
    packages=find_packages(include=['cli', 'cli.*']),
    entry_points={
        'console_scripts': [
            'depmap=cli.cli:main',  # Assuming cli.py contains a main function
        ],
    },
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)

