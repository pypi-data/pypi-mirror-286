from setuptools import find_packages, setup

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.8',
]
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent


setup(
    name='kkba_mathUtils',
    packages=find_packages(include=['kkba_mathUtils']),
    version='2.0.0',
    description='My basic mathematics Python library',
    author='Kuate Brayan',
    author_email='brayanarmel@gmail.com',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    classifiers=classifiers,
    keywords='mathematics library',
    # other arguments omitted
    long_description=open('README.md').read(),
)