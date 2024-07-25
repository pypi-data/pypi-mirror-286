# setup.py
from setuptools import setup, find_packages

setup(
    name="i2c_can",
    version="0.0.1",
    description="Tire Pressure Monitoring System Python Library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sam Conway",
    author_email="pypi@invertica.co.uk",
    url="https://github.com/samskjord/ic2_can",  # Update with your repository URL
    packages=find_packages(),
    install_requires=[
        "smbus2",
    ],
    entry_points={
        "console_scripts": [
            "example_multiple_pids=examples.example_multiple_pids:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
