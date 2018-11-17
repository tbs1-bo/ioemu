# setup.py
# https://packaging.python.org/tutorials/packaging-projects/

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ioemu",
    version="0.1.1",
    author="Marco Bakera",
    author_email="marco@bakera.de",
    description="IO Emulator with LEDs and buttons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tbs1-bo/ioemu",
    packages=setuptools.find_packages(),
    package_data={
        '': ['*png'],  # include image files for all packages
    },
    entry_points = {
        'console_scripts': [],
        'gui_scripts': ['ioemu = ioemu:run']
    },
    install_requires='PyQt5>=5.11.3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
