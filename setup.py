import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="market_data_extraction_tool",
    version="1.0",
    author="LMquentinLR",
    description="Script to download intraday, daily and option market data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LMquentinLR/market_data_extraction_tool",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)