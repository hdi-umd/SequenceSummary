from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sequence-summary",
    version="0.1.0",
    author="Kazi Tasnim Zinat",
    author_email="kzintas@und.edu",
    description="Visual summarization techniques for event sequences",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hdi-umd/sequence-summary",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License ::  MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "datasketch",
        "sklearn",
        "certifi",
        "spmf",
    ],
    extras_require={
        "dev": [
            "pytest",
            "memory_profiler",
        ],
        "viz": [
            "react",
            "bootstrap",
        ],
    },
    entry_points={
        "console_scripts": [
            "run-coreflow=sequence_summary.mining.coreflow.main:main",
            "run-sententree=sequence_summary.mining.sententree.main:main",
            "run-sequencesynopsis=sequence_summary.mining.sequencesynopsis.main:main",
            "run-all=sequence_summary.run_all:main",
        ],
    },
)
