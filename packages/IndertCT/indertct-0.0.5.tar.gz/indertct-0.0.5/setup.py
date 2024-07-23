from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.5'
DESCRIPTION = 'Package for IndertCT´s Api'
LONG_DESCRIPTION = 'A package to help you use IndertCT´s API'


setup(
    name="IndertCT",
    version=VERSION,
    author="Dinis Moreira",
    author_email="jusupaq@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'IndertCT', 'cryptocurrency', 'money', 'market forecast', 'crypto', 'crypto market', 'cryptocurrency market', 'API', 'Integration', 'IndertCT integration'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
