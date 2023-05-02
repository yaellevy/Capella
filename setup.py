import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Capella",
    version="1.0.4",
    author="AlexSpradling",
    author_email="alexspradling@gmail.com",
    description="Capella Beta",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlexSpradling/Capella.git",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'scipy',
        'skyfield',
        'tkinter',
        'pytz',
        'datetime',
        'tabulate',
        'ttkwidgets',
        'pyperclip',
        'ctypes',
        'ttkbootstrap',
        'collections',
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)