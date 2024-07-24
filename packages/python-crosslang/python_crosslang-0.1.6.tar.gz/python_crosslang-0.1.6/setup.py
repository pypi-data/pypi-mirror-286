from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='python-crosslang',
    version='0.1.6',
    author='fl9ppy',
    author_email='adi.calinescu16@gmail.com',
    description='A Python library to run code from multiple programming languages.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fl9ppy/crosslang',
    packages=find_packages(include=['crosslang', 'crosslang.*']),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[],
)
