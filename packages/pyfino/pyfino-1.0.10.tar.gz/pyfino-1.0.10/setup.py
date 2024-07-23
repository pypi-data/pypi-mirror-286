# coding: utf-8

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pyfino',
    version='1.0.10',
    description='可以实现节点自动化消息协同的框架', 
    author='xuwh',  
    author_email='xuwhdev@gmail.com',
    url='http://xuwh.net',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
)