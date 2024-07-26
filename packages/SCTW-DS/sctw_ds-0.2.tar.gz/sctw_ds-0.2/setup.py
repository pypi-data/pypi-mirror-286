from setuptools import find_packages, setup

setup(
    name="SCTW_DS",
    version="0.2",
    packages=find_packages(),  # Automatically includes all sub-packages
    install_requires=[
        "numpy>=1.21.0",  # For numerical operations
        "pandas>=1.3.0",  # For data manipulation and analysis
    ],
    entry_points={
        "console_scripts": [
            # Example: 'my_script=my_package.module:main_func'
            # Add any CLI commands if you have any scripts to expose
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
