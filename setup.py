from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='steamcrawl',
    version='0.1.9',
    description='A package that helps extract Steam store and community market data as pandas DataFrame for better readabilty and usability.',
    packages=["steamcrawl"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Hungreeee',
    author_email='hungmnguyen13102003@gmail.com',
    license='MIT',
    url='https://github.com/Hungreeee/steamcrawl',
    install_requires=['requests', 'pandas', 'selenium-wire'],
    classifiers = []
)