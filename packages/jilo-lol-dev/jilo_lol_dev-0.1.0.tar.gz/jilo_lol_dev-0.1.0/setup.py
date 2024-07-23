from setuptools import setup, find_packages

setup(
    name="jilo_lol_dev",  # Replace with your package name
    version="0.1.0",  # Replace with your version number
    description="A Python package for performing math operation with joy inside of you",  # Replace with a description
    author="Jilo Developer",
    author_email="chibuezeadeyemi@gmail.com",
    packages=find_packages(),
    install_requires=[  # List any dependencies here
        "requests",
    ],
)