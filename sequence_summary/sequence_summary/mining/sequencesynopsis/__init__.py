"""
SequenceSynopsis mining implementation.

This module provides implementations of the SequenceSynopsis algorithm for
optimized visual summaries using the minimum description length principle.
"""

# Import all implementations
from .sequence_synopsis_miner import SequenceSynopsisMiner as BaseSequenceSynopsisMiner
from .sequence_synopsis_miner_with_lsh import (
    SequenceSynopsisMiner as LSHSequenceSynopsisMiner,
)
from .sequence_synopsis_miner_with_weighted_lsh import (
    SequenceSynopsisMiner as WeightedLSHSequenceSynopsisMiner,
)

# Make the weighted LSH version the default
SequenceSynopsisMiner = WeightedLSHSequenceSynopsisMiner

# Export all implementations
__all__ = [
    "SequenceSynopsisMiner",
    "BaseSequenceSynopsisMiner",
    "LSHSequenceSynopsisMiner",
    "WeightedLSHSequenceSynopsisMiner",
]
