from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess, sys

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        subprocess.call([sys.executable, '-m', 'emtechstack.post_install'])


setup(
    name="emtechstack",
    version="0.0.99",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "black",
        "PyYAML",
        "requests",
        "tabulate",
        "termcolor",
    ],
    entry_points={
        "console_scripts": [
            "emtechstack=emtechstack.cli:cli",
            "e9k=emtechstack.cli:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
