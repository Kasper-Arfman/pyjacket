#!/usr/bin/env python
from setuptools import setup, find_packages


import subprocess
# import setuptools
import os

remote_version = subprocess.run(['git', 'describe', '--tags'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

print(remote_version)

# assert '.' in remote_version

# assert os.path.isfile('cf_remote/version.py')


# with open('cf_remote/VERSION', 'w', encoding='utf-8') as fh:
#     fh.write(f'{remote_version}\n')

exit()


setup(
    name='pyglet',
    version=remote_version,
    author='Alex Holkner',
    author_email='Alex.Holkner@gmail.com',
    url='http://pyglet.readthedocs.org/en/latest/',
    download_url='http://pypi.python.org/pypi/pyglet',
    project_urls={
        'Documentation': 'https://pyglet.readthedocs.io/en/latest',
        'Source': 'https://github.com/pyglet/pyglet',
        'Tracker': 'https://github.com/pyglet/pyglet/issues',
    },
    description='Cross-platform windowing and multimedia library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # Package info
    packages=['pyglet'] + ['pyglet.' + pkg for pkg in find_packages('pyglet')],

    # Add _ prefix to the names of temporary build dirs
    options={'build': {'build_base': '_build'}, },
    zip_safe=True,
)