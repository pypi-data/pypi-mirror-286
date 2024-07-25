from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
here = Path(__file__).parent

# Read the requirements from requirements.txt
def parse_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name='utility-lib-python',
    version='0.1.1',
    description='A collection of utility scripts for working with files, Excel, logging, and database connections.',
    long_description="""Welcome to the Python Utils repository! This project contains a collection of utility scripts written in Python for various purposes. Each script focuses on specific functionalities that can be reused across different projects.
    Check GitHub for more details.""",
    long_description_content_type='text/markdown',
    author='Hirushiharan',
    author_email='hirushiharant@gmail.com',
    url='https://github.com/hirushiharan/python-utility-functions.git',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
