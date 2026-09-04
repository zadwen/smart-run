from setuptools import find_packages, setup

setup(
    name="smart-run",
    version="0.1.0",
    description="Detects a downloaded file's type and runs it the right way.",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "smart-run=smart_run.cli:main",
        ],
    },
    python_requires=">=3.7",
)
