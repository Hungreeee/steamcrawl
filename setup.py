from setuptools import setup

with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    name='steammy',
    version='0.1.0',
    description='A package that helps extract Steam market data as pandas DataFrame for better readabilty and usage.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Hungreeee',
    author_email='hungmnguyen13102003@gmail.com',
    license='MIT',
    url='https://github.com/Hungreeee/steammy',
    install_requires=['requests', 'pandas'],
    python_requires='>=3.5',
)