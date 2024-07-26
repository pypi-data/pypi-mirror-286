from setuptools import setup, find_packages

setup(
    name='auto8',
    version='0.1.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'flake8',
    ],
    entry_points={
        'console_scripts': [
            'auto8=auto8.main:main',
        ],
    },
    author='Naser Jamal',
    author_email='naser.dll@hotmail.com',
    description='A tool to automatically fix flake8 issues',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/naserjamal/auto8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)