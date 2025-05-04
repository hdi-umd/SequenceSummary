"""
Core components for event sequence summarization techniques.

This module provides the fundamental data structures and algorithms used
by the various summarization techniques, including:

- Node: Base class for tree and graph structures
- Pattern: Representation of event patterns in sequences
- Graph: Structures for representing visualization outputs
- Cluster: Grouping of similar sequences
"""

from .cluster import Cluster
from .graph import Graph, RawNode, Links
from .node import Node, TreeNode, GraphNode
from .pattern import Pattern
from .queue_elements import QueueElements
