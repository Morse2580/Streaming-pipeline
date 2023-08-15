from pathlib import Path
from setuptools import find_namespace_packages, setup

# Load packages from requirements.txt
BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt"), "r") as file:
    required_packages = [ln.strip() for ln in file.readlines()]

# setup.py
test_packages = [
    "pytest==7.4.0",
]

# Define our package
setup(
    name="finnhub-producer",
    version=0.1,
    description="Extracting data from Finnhub API using Kafka subscription",
    author="Moses Njau",
    python_requires=">=3.7",
    packages=find_namespace_packages(),
    install_requires=[required_packages],
    extras_require={
            "dev": test_packages,
            "test": test_packages
        }
)

