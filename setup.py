import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Capella",
    version="1.0.3",
    author="AlexSpradling",
    author_email="alexspradling@gmail.com",
    description="Capella Beta",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlexSpradling/Capellav.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)