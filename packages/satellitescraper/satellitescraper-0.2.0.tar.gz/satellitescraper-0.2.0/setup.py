import setuptools
import re
import ast
with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="satellitescraper",
    version="0.2.0",
    author="Mostafa Mabrok",
    author_email="mostafa.m.mabrok@gmail.com",
    description="Python Package for Scraping Sattelite Image Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mostafamabrok/longitude",
    install_requires=['certifi','chardet','chromedriver-autoinstaller','idna',
                      'numpy','requests','selenium','tqdm','urllib3', 
                      'opencv-python', 'webdriver_manager'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

