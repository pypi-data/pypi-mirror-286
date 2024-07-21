from setuptools import setup, find_packages

setup(
    name="wivi-graph-lib",
version="2.2.4",
    packages=find_packages(),
    install_requires=[
        "requests",
        "graphql-core",
    ],
    author="Awais Ayub",
    author_email="aayub@intrepidcs.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
