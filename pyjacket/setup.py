from setuptools import setup, find_packages

setup(
    name='pyjacket',
    version='0.2',
    license='MIT',
    author="Kasper Arfman",
    author_email='kasper.arf@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Kasper-Arfman/pyjacket',
    keywords='example project',
    install_requires=[
      ],

)