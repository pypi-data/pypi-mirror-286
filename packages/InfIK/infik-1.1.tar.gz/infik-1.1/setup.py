from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="InfIK",
    version="1.1",
    description="A flexible inverse kinematics solver that supports any number of servo motors in series",
    long_description=description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "numpy>=2.0.0"
    ]
)