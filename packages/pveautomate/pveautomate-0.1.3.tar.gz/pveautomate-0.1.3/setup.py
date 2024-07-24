from setuptools import setup, find_packages

setup(
    name="pveautomate",
    version="0.1.3",
    description="A package to automate Proxmox VE tasks",
    long_description=open("README.md").read()
    + "\n# Usage Docs:\n"
    + open("DOCS.md").read(),
    long_description_content_type="text/markdown",
    author="Matt Compton",
    author_email="matt@alchemicode.com",
    url="https://github.com/alchemicode/pveautomate",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
