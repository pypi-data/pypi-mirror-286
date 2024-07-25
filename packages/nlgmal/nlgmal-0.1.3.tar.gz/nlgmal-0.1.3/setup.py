from setuptools import setup, find_packages

setup(
    name='nlgmal',
    version='0.1.3',
    packages=find_packages(where='src'),  # Locate packages within 'src'
    package_dir={'': 'src'},  # Specify the source directory
    description='A custom cryptographic package using the NLGdecimal number system.',
    author='NLG SAKIB',
    author_email='nlgarts@outlook.com',
    license='MIT',
    install_requires=[],
)
