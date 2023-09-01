GIT_USER = 'Kasper-Arfman'
NAME = 'testpyjacket'


import setuptools
import subprocess
import os

remote_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)

if "-" in remote_version:
    # when not on tag, git describe outputs: "1.3.3-22-gdf81228"
    # pip has gotten strict with version numbers
    # so change it to: "1.3.3+22.git.gdf81228"
    # See: https://peps.python.org/pep-0440/#local-version-segments
    v,i,s = remote_version.split("-")
    remote_version = v + "+" + i + ".git." + s

# assert "-" not in remote_version
# assert "." in remote_version
# assert os.path.isfile("src/version.py")
# with open("src/VERSION", "w", encoding="utf-8") as fh:
    # fh.write("%s\n" % remote_version)

setuptools.setup(
    name=NAME,
    version=remote_version,
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
    # install_requires=[],

    # # Add _ prefix to the names of temporary build dirs
    # options={'build': {'build_base': '_build'}, },
    # zip_safe=True,
)