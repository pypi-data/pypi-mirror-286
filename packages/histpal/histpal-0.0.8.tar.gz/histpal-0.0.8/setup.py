
from setuptools import setup
from setuptools import setup, find_packages

setup(
    name='histpal',
    version='0.0.8',
    author='Ahmed Helmy',
    author_email='a7med.7assaan@gmail.com',
    description='A Python library that empowers you to explore and utilize color palettes from various historical civilizations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/A7med-7elmy/histpal',  
    packages=find_packages(),
    
    classifiers=[
        'Programming Language :: Python :: 3',
          'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        "setuptools>=61.0",
        "dependency3; python_version>='3'", 
    ],
)
