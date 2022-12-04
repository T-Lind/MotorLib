from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.3'
DESCRIPTION = '12V Motor control for robotics.'
LONG_DESCRIPTION = ''

# Setting up
setup(
    name="pymotorlib",
    version=VERSION,
    author="Tiernan Lindauer",
    author_email="<tiernanxkl@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['RPi.GPIO'],
    keywords=['python', 'robotics', 'motors'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)