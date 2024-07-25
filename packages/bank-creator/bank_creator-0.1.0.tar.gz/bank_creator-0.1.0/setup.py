# Import the setup and find_packages functions from setuptools
from setuptools import setup, find_packages

# Call the setup function, which is the primary function for setting up the package
setup(
    # The name of the package
    name="bank_creator",
    # The version of the package
    version="0.1.0",
    # The author's name
    author="winston mhango",
    # The author's email address
    author_email="winstonmhango23@gmail.com",
    # A short description of the package
    description="A comprehensive banking system package with accounts, loans, rewards, and utilities.",
    # A long description of the package, read from the README.md file
    long_description=open("README.md").read(),
    # The format of the long description
    long_description_content_type="text/markdown",
    # The URL for the project's homepage
    url="https://github.com/winstonmhango23/bank_creator",
    # Automatically find all packages within the current directory and subdirectories
    packages=find_packages(),
    # Classifiers help users find your project by categorizing it
    classifiers=[
        # The programming language used
        "Programming Language :: Python :: 3",
        # The license under which the package is distributed
        "License :: OSI Approved :: MIT License",
        # The operating systems on which the package can run
        "Operating System :: OS Independent",
    ],
    # Specify the minimum Python version required
    python_requires=">=3.6",
    # A list of dependencies required to use the package
    install_requires=[
        # List any dependencies here, e.g., 'requests', 'numpy'
        # For now, this is left empty
    ],
)
