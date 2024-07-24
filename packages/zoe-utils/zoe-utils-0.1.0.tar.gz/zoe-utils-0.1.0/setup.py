from pathlib import Path

from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='zoe-utils',
    version='0.1.0',
    author='Pavlo Sevidov',
    author_email='pavlo.sevidov@datavise.ai',
    description='A Zeo utility library for working with Prefect',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pavlo-sevidov-datavise/zoe-utils',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
