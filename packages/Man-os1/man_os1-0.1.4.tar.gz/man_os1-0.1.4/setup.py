from setuptools import setup, find_packages

# Read the contents of README.md for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Man_os1",  # Replace with your own library name
    version="0.1.4",
    author="Ahmd ZOUITANE",
    author_email="zouitane.ahmed02@gmail.com",
    description="#Role:\nThe `Man_os1` library provides a set of utility functions for file and directory management tasks such as creating, removing, renaming, and listing files and directories. It also includes functions for file operations like reading and writing, as well as retrieving system and environmental information.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZOUITANE-Ahmed/Man_os1.git",  # Replace with the URL of your GitHub repo
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "colorama>=0.4.4",
    ],
)
