from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'Statistics for osu! tournaments'

# Setting up
setup(
    name="osustats",
    version=VERSION,
    author="Le Duc Minh (ldminh4354)",
    author_email="ducminh0401@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=['pandas', 'requests'],
    keywords=['python', 'osu!', 'stats', 'statistics'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)