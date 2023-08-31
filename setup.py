#!/usr/bin/env python
from setuptools import setup, find_packages


import subprocess
# import setuptools
# import os

remote_version = subprocess.run(['git', 'describe', '--tags'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
# remote_version = '0.0.3'

# print(remote_version)

# assert '.' in remote_version

# assert os.path.isfile('cf_remote/version.py')


# with open('cf_remote/VERSION', 'w', encoding='utf-8') as fh:
#     fh.write(f'{remote_version}\n')

# exit()


setup(
    name='pyjacket',
    version=remote_version,
    author='Kasper Arfman',
    author_email='Kasper.arf@gmail.com',
    
    # download_url='http://pypi.python.org/pypi/kaspy',
    # project_urls={
    #     # 'Documentation': 'https://pyglet.readthedocs.io/en/latest',
    #     'Source': 'https://github.com/Kasper-Arfman/kaspy',
    #     'Tracker': 'https://github.com/pyglet/Kasper-Arfman/issues',
    # },
    description='Lorem ipsum',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Kasper-Arfman/kaspy',
    # license='MIT'
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent"
    ],
    # python_requires="",
    # entry_points=[],
    # install_requires=[],

    # # Add _ prefix to the names of temporary build dirs
    # options={'build': {'build_base': '_build'}, },
    # zip_safe=True,
)