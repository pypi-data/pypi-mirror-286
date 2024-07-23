from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
  name='asyncro',
  version='0.0.1',
  author='justflade & nekit270',
  author_email='apbclub142@gmail.com',
  description='Simple async module based on threading.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/fladegh/asyncflow',
  packages=find_packages(),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='async thread threads',
  project_urls={
    'GitHub': 'https://github.com/fladegh/asyncflow'
  },
  python_requires='>=3.8'
)