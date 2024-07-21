import   setuptools 

# Read the contents of README.md for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Man_os1",  # Replace with your own library name
    version="0.1.1",
    author="Ahmed ZOUITANE",
    author_email="zouitane.ahmed02@gmail.com",
    description="'Man_os1' is a Python library for managing files and folders easily and quickly. The library includes multiple functions for creating, reading, writing, and deleting files and folders, as well as changing directories and listing directory contents.",
    url="https://github.com/ZOUITANE-Ahmed/Man_os1.git",  # Replace with the URL of your GitHub repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
