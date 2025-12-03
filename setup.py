"""
Setup script for DFW RealtyVest AVM
Makes the src/ directory installable as a package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dfw-realtyvest-avm",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Hyper-accurate Automated Valuation Model for DFW real estate",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dfw-realtyvest-avm",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pandas>=2.1.0",
        "numpy>=1.24.0",
        "lightgbm>=4.1.0",
        "xgboost>=2.0.0",
        "scikit-learn>=1.3.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "selenium>=4.15.0",
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "geopy>=2.4.0",
        "folium>=0.15.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
        "python-dateutil>=2.8.0",
        "fuzzywuzzy>=0.18.0",
        "python-Levenshtein>=0.23.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
            "jupyter>=1.0.0",
            "ipykernel>=6.26.0",
        ],
        "ui": [
            "streamlit>=1.28.0",
            "streamlit-folium>=0.15.0",
            "plotly>=5.18.0",
        ],
    },
)