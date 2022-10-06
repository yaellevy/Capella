from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Celestial Navigation Aid'
LONG_DESCRIPTION = 'A package that allows for fast, simple Astro Navigation'

# Setting up
setup(
    name="Capella",
    version=VERSION,
    author="Alex Spradling",
    author_email="<alexspradling@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'matplotlib', 'scipy', 'skyfield', 'geomag', 'tabulate', 'ttkbootstrap',
                      'pyperclip'],
    keywords=['python', 'navigation', 'astronomy', 'statistics', 'maritime', 'shipping'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Mariners",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)