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
        "scikit-learn",
        "certifi",
        "spmf",
    ],
    # Different implementation variants as extras
    extras_require={
        # Base sequence synopsis without LSH
        "basic": [],
        # Sequence synopsis with LSH
        "lsh": ["datasketch"],
        # Sequence synopsis with weighted LSH
        "weighted-lsh": ["datasketch", "scikit-learn"],
        # Include all sequence synopsis implementations
        "all-synopsis": ["datasketch", "scikit-learn"],
        # Development dependencies
        "dev": ["pytest", "memory_profiler"],
    },
    # Command-line entry points for different implementations
    entry_points={
        "console_scripts": [
            "run-coreflow=sequence_summary.mining.coreflow.main:main",
            "run-sententree=sequence_summary.mining.sententree.main:main",
            # Basic sequence synopsis
            "run-sequencesynopsis=sequence_summary.mining.sequencesynopsis.main:run_basic",
            # LSH implementation
            "run-sequencesynopsis-lsh=sequence_summary.mining.sequencesynopsis.main:run_with_lsh",
            # Weighted LSH implementation
            "run-sequencesynopsis-weighted=sequence_summary.mining.sequencesynopsis.main:run_with_weighted_lsh",
            # Run all techniques
            "run-all=sequence_summary.run_all:main",
        ],
    },
)
