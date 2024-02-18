from setuptools import setup, find_packages

setup(
    name="sipro",
    version="1.0.0",
    packages=find_packages(),
    description="A very simple profiler for Python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/eliasffyksen/sipro",
    author="Elias F. Fyksen",
    author_email="github@fyksen.net",
    license="MIT",
    install_requires=[],
    include_package_data=True,
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)