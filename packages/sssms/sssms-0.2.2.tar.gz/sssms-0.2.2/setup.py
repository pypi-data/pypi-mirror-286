from setuptools import setup, find_packages
import os 

with open(f"{os.path.join(os.path.dirname(__file__),'README.md')}", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sssms",
    version='0.2.2',
    author="Joel Yisrael",
    author_email="joel@sss.bot",
    description="Self-Service SMS via eMail",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/schizoprada/sssms",
    packages=find_packages(),
    install_requires=[
        "click",
        "requests",
        "beautifulsoup4",
        "rich",
        "pyyaml",
        "cryptography",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "sssms=sssms.main:cli",
        ],
    },
)