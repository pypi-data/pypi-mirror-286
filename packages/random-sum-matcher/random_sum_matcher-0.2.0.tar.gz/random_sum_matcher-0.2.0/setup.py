from setuptools import setup, find_packages

setup(
    name="random_sum_matcher",
    version="0.2.0",
    author="zimu zhang",
    author_email="zhang0418zimu@163.com",
    description="A simple addition calculator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
