import setuptools

__version__ = '0.0.1'

GIT_USER = 'Kasper-Arfman'
NAME = 'pyjacket'

setuptools.setup(
    name=NAME,
    version=__version__,
    author='Kasper Arfman',
    author_email='Kasper.arf@gmail.com',
    
    download_url=f'http://pypi.python.org/pypi/{NAME}',
    project_urls={
        # 'Documentation': 'https://pyglet.readthedocs.io/en/latest',
        'Source': f'https://github.com/{GIT_USER}/{NAME}',
        'Tracker': f'https://github.com/{GIT_USER}/{NAME}/issues',
    },
    description='Lorem ipsum',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url=f'https://github.com/{GIT_USER}/{NAME}',
    # license='MIT'
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent"
    ],
    # python_requires="",
    # entry_points=[],
    install_requires=[],

    # # Add _ prefix to the names of temporary build dirs
    # options={'build': {'build_base': '_build'}, },
    # zip_safe=True,
)