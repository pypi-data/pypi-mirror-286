from setuptools import setup, find_packages

setup(
    name="yodi_pys",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Add dependencies here.
        # e.g. 'numpy>=1.11.1'
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Yodi Dev Team",
    author_email="djdefodji@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)