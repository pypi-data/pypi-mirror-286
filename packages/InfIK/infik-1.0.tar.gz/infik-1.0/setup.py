from setuptools import setup, find_packages

setup(
    name="InfIK",
    version="1.0",
    description="A flexible inverse kinematics solver that supports any number of servo motors in series",
    packages=find_packages(),
    install_requires=[
        "numpy>=2.0.0"
    ]
)