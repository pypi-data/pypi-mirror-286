from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
  name='pyshapearea',
  version='0.0.1',
  author='V1sl3t',
  author_email='suppes214@gmail.com',
  description='Module for calculating the area of shapes',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/V1sl3t/PyShapeArea',
  packages=find_packages(),
  classifiers=[
    'Programming Language :: Python :: 3.11',
  ],
  project_urls={
    'GitHub': 'https://github.com/V1sl3t'
  },
  python_requires='>=3.6'
)
