from setuptools import setup, find_packages

setup(
    name="dockrich",
    version="0.4",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "dockrich = dockrich.dockrich:main",
        ],
    },
    install_requires=[
        "rich",
    ],
    python_requires=">=3.6",
    author="Prasaanth Sakthivel",
    author_email="prasaanth@gmail.com",
    description="A tool to pretty print Docker command outputs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dockrich",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)