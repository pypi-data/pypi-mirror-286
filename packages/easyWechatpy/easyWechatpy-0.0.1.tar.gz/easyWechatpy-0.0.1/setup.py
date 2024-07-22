# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = '0.0.1'

setup(
    name="easyWechatpy",  # package name
    version=VERSION,  # package version
    author="Lei Cui",
    author_email="cuilei798@qq.com",
    maintainer="Lei Cui",
    maintainer_email="cuilei798@qq.com",
    license="MIT License",
    platforms=["linux"],
    url="https://github.com/xleizi/easyWechatpy",
    description="The purpose of the creation of this package is to make bioinformatics analysis simpler.",
    long_description=open("README.md").read(),
    packages=find_packages(),
    zip_safe=False,
    # entry_points={
    #     "console_scripts": [
    #         "easyBio=easyBio.easyBio:main",
    #     ]
    # },
    install_requires=[
        "requests",
    ],
    package_data={"Utils": ["Utils/*"]},
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3",
)
