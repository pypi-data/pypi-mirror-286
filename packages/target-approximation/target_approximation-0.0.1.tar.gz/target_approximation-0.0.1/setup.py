from setuptools import setup

install_requires = [
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'tools-io',
    ]

setup(
    name='target-approximation',
    version='0.0.1',
    description='Python implementation of the Target-Approximation-Model.',
    author='Paul Krug',
    url='https://github.com/paul-krug/target-approximation',
    license='MIT',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    packages=['target_approximation'],
    install_requires=install_requires
)