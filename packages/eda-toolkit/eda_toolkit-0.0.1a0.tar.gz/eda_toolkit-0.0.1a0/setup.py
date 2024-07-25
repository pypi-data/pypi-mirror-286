from setuptools import setup, find_packages
import codecs

with codecs.open("README_min.md", "r", "utf-8") as fh:
    long_description = fh.read()

setup(
    name="eda_toolkit",
    version="0.0.1a",
    author="Leonid Shpaner, Oscar Gil",
    author_email="lshpaner@ucla.edu",
    description="A Python library for EDA (directory management, some data preprocessing, reporting, visualizations, and more)",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Type of the long description
    package_dir={"": "src"},  # Directory where your package files are located
    # Automatically find packages in the specified directory
    packages=find_packages(where="src"),
    project_urls={  # Optional
        "Leonid Shpaner Website": "https://www.leonshpaner.com",
        "Oscar Gil Website": "https://www.oscargildata.com",
        "Source Code": "https://github.com/lshpaner/eda_kit/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # Classifiers for the package
    python_requires=">=3.6",  # Minimum version of Python required
    install_requires=[
        "jinja2>=3.1.4",  # Minimum version of jinja2 required
        "numpy>=1.21.6",  # Minimum version of numpy required
        "pandas>=1.3.5",  # Minimum version of pandas required
        "matplotlib>=3.5.3",  # Minimum version of matplotlib required
        "seaborn>=0.12.2",  # Minimum version of seaborn required
        "xlsxwriter>=3.2.0",  # Minimum version of xlsxwriter required
    ],
)
