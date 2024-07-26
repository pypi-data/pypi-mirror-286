import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="finalse-sdk",
    version="1.0.0",
    author="Finalse Cloud Services",
    author_email="opensource@finalse.com",
    description="Sdk to access Finalse Cloud platform in Python based environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/finalse/sdk-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)