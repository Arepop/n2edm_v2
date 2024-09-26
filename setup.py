import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="n2edm",
    version="0.1.0",
    author="Arkadiusz Popczak",
    author_email="arepop@arepop.com",
    description="Package created for n2EDM experiment to schedule mesurement.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=[""],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
    ],
)
